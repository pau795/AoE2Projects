"""Protocol, camera identity, and binary preview regression checks (no hardware)."""

import configparser
import io
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

from mediamtx_sender import (
    DEFAULT_OPTIONS, PREVIEW_HEIGHT, PREVIEW_WIDTH, application_path, build_command, camera_index,
    destination, find_ffmpeg, list_cameras, load_options, read_log_lines, read_ppm, save_options,
)


class SenderTests(unittest.TestCase):
    def test_packaged_app_uses_executable_location_for_external_files(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "mediamtx_sender.exe"
            ffmpeg = Path(directory) / "ffmpeg.exe"
            ffmpeg.touch()
            with patch("mediamtx_sender.sys.frozen", True, create=True), \
                    patch("mediamtx_sender.sys.executable", str(executable)):
                self.assertEqual(application_path(), executable.resolve())
                self.assertEqual(find_ffmpeg(), str(ffmpeg.resolve()))

    def test_log_delimiters_partial_utf8_and_final_unterminated_line(self):
        class ChunkedStream(io.BytesIO):
            def read1(self, size=-1):
                return super().read1(min(size, 2))
        stream = ChunkedStream("first\rsecond\r\nCámara\nlast".encode())
        self.assertEqual(list(read_log_lines(stream)), ["first", "second", "Cámara", "last"])

    def test_log_arrives_before_writer_closes_pipe(self):
        for buffering, delimiter in ((buffering, delimiter)
                                     for buffering in (0, -1)
                                     for delimiter in (b"\r", b"\n", b"\r\n")):
            with self.subTest(buffering=buffering, delimiter=delimiter):
                reader_fd, writer_fd = os.pipe()
                stream = os.fdopen(reader_fd, "rb", buffering=buffering)
                received = threading.Event()
                messages = []

                def consume():
                    for line in read_log_lines(stream):
                        messages.append(line)
                        received.set()

                worker = threading.Thread(target=consume, daemon=True)
                worker.start()
                try:
                    os.write(writer_fd, b"live diagnostic" + delimiter)
                    self.assertTrue(received.wait(2), "Log was buffered until EOF")
                    self.assertEqual(messages, ["live diagnostic"])
                finally:
                    os.close(writer_fd)
                    worker.join(timeout=2)
                    stream.close()

    def test_rtsp_ipv6_and_credentials(self):
        self.assertEqual(
            destination("::1", "8554", "live/camera", "RTSP / TCP", "a@b", "p:/"),
            "rtsp://a%40b:p%3A%2F@[::1]:8554/live/camera",
        )

    def test_rtmp_url(self):
        self.assertEqual(destination("192.168.1.20", "1935", "webcam", "RTMP"),
                         "rtmp://192.168.1.20:1935/webcam")

    def test_bad_destination(self):
        for host, port, path in [("rtsp://localhost", "8554", "webcam"),
                                 ("localhost:8554", "8554", "webcam"),
                                 ("localhost", "65536", "webcam"),
                                 ("localhost", "0", "webcam"),
                                 ("localhost", "8554", ""),
                                 ("localhost", "8554", "../webcam")]:
            with self.subTest(host=host, port=port, path=path), self.assertRaises(ValueError):
                destination(host, port, path, "RTSP / TCP")

    def test_duplicate_camera_identities_and_audio_exclusion(self):
        stderr = '\n'.join([
            '[dshow] "USB Camera" (video)', '[dshow] Alternative name "@device_one"',
            '[dshow] "USB Camera" (video)', '[dshow] Alternative name "@device_two"',
            '[dshow] "Microphone" (audio)', '[dshow] Alternative name "@audio"',
        ])
        with patch("mediamtx_sender.subprocess.run", return_value=
                   subprocess.CompletedProcess([], 1, "", stderr)):
            self.assertEqual(list_cameras("ffmpeg.exe"),
                             [("USB Camera", "@device_one"), ("USB Camera", "@device_two")])

    def command(self, protocol="RTSP / TCP", url=None, encoder="libx264"):
        return build_command("ffmpeg.exe", "@device_camera", "Camera default", 30,
                             encoder, 2500, protocol, url)

    def test_preview_only_has_one_camera_input(self):
        cmd = self.command()
        self.assertEqual(cmd.count("-i"), 1)
        self.assertNotIn("-video_size", cmd)
        self.assertNotIn("libx264", cmd)
        self.assertEqual(cmd[-1], "pipe:1")

    def test_camera_input_omits_output_only_queue_option(self):
        cases = [("RTSP / TCP", None),
                 ("RTSP / TCP", "rtsp://server:8554/webcam"),
                 ("RTSP / UDP", "rtsp://server:8554/webcam"),
                 ("RTMP", "rtmp://server:1935/webcam")]
        for protocol, url in cases:
            with self.subTest(protocol=protocol, url=url):
                cmd = self.command(protocol, url)
                input_options = cmd[1:cmd.index("-i")]
                self.assertNotIn("-thread_queue_size", input_options)
                self.assertEqual(input_options[-4:], ["-f", "dshow", "-framerate", "30"])

    def test_rtsp_transport_and_shared_preview(self):
        for protocol, transport in [("RTSP / TCP", "tcp"), ("RTSP / UDP", "udp")]:
            with self.subTest(protocol=protocol):
                cmd = self.command(protocol, "rtsp://server:8554/webcam")
                self.assertEqual(cmd[cmd.index("-rtsp_transport") + 1], transport)
                self.assertEqual(cmd.count("-i"), 1)
                self.assertEqual(cmd.count("-map"), 2)
                self.assertIn("rtsp", cmd)
                self.assertEqual(cmd[-1], "pipe:1")

    def test_rtmp_gpu_does_not_use_x264_options(self):
        cmd = self.command("RTMP", "rtmp://server:1935/webcam", "h264_nvenc")
        self.assertIn("flv", cmd)
        self.assertNotIn("-rtsp_transport", cmd)
        self.assertNotIn("-tune", cmd)
        self.assertIn("h264_nvenc", cmd)

    def test_rtsp_packet_size_scoped_to_stream_output(self):
        url = "rtsp://server:8554/webcam"
        for protocol in ("RTSP / TCP", "RTSP / UDP"):
            with self.subTest(protocol=protocol):
                cmd = self.command(protocol, url)
                packet_index = cmd.index("-pkt_size")
                self.assertEqual(cmd[packet_index + 1], "1200")
                self.assertGreater(packet_index, cmd.index("-i"))
                self.assertLess(packet_index, cmd.index(url))
                self.assertNotIn("-pkt_size", cmd[cmd.index(url) + 1:])
        self.assertNotIn("-pkt_size", self.command())
        self.assertNotIn("-pkt_size", self.command("RTMP", "rtmp://server:1935/webcam"))

    def test_custom_packet_size_and_validation(self):
        args = ("ffmpeg", "camera", "Camera default", 30, "libx264", 2500,
                "RTSP / TCP", "rtsp://server:8554/webcam")
        cmd = build_command(*args, packet_size=1400)
        self.assertEqual(cmd[cmd.index("-pkt_size") + 1], "1400")
        for value in (0, 255, 65508):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_command(*args, packet_size=value)

    def test_config_round_trip_with_literal_percent_and_camera_path(self):
        options = DEFAULT_OPTIONS | {
            "ffmpeg": r"C:\Program Files\FFmpeg\ffmpeg.exe", "host": "192.168.1.12",
            "port": "9554", "path": "live/webcam", "protocol": "RTSP / UDP",
            "encoder": "NVIDIA GPU (NVENC)", "size": "1920x1080", "fps": "60",
            "bitrate": "5000", "packet_size": "1400", "username": "user%name",
            "camera_name": "Cámara USB", "camera_id": r"@device_pnp_\\?\usb#camera\global",
            "password": "p%ss", "remember_password": "true",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sender.cfg"
            save_options(options, path)
            self.assertEqual(load_options(path), options)

    def test_config_password_requires_opt_in_and_can_be_removed(self):
        options = DEFAULT_OPTIONS | {"password": "secret", "remember_password": "true"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sender.cfg"
            save_options(options, path)
            self.assertEqual(load_options(path)["password"], "secret")
            options["remember_password"] = "false"
            save_options(options, path)
            self.assertNotIn("secret", path.read_text(encoding="utf-8"))
            self.assertEqual(load_options(path)["password"], "")

    def test_missing_config_defaults_and_unknown_choices(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sender.cfg"
            self.assertEqual(load_options(path), DEFAULT_OPTIONS)
            save_options(DEFAULT_OPTIONS | {"encoder": "missing encoder", "fps": "999"}, path)
            loaded = load_options(path)
            self.assertEqual(loaded["encoder"], DEFAULT_OPTIONS["encoder"])
            self.assertEqual(loaded["fps"], DEFAULT_OPTIONS["fps"])

    def test_config_atomic_write_failure_preserves_existing_options(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sender.cfg"
            save_options(DEFAULT_OPTIONS | {"host": "old-host"}, path)
            with patch("mediamtx_sender.os.replace", side_effect=PermissionError("locked")):
                with self.assertRaises(PermissionError):
                    save_options(DEFAULT_OPTIONS | {"host": "new-host"}, path)
            self.assertEqual(load_options(path)["host"], "old-host")
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_malformed_config_reports_parser_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sender.cfg"
            path.write_text("not an INI file", encoding="utf-8")
            with self.assertRaises(configparser.Error):
                load_options(path)

    def test_camera_restore_uses_identity_before_name_or_order(self):
        devices = [("USB Camera", "device_b"), ("USB Camera", "device_a")]
        self.assertEqual(camera_index(devices, "device_a", "USB Camera"), 1)
        self.assertEqual(camera_index(devices, "missing", "USB Camera"), 0)
        self.assertEqual(camera_index(devices, "missing", "missing"), 0)
        self.assertEqual(camera_index([], "device_a", "USB Camera"), -1)

    def test_ppm_binary_payload_and_eof(self):
        # Binary data may contain whitespace, newlines, and header-like bytes.
        frame = (f"P6\n{PREVIEW_WIDTH} {PREVIEW_HEIGHT}\n255\n".encode()
                 + (bytes(range(256)) * (PREVIEW_WIDTH * PREVIEW_HEIGHT * 3 // 256 + 1))
                 [:PREVIEW_WIDTH * PREVIEW_HEIGHT * 3])
        stream = io.BytesIO(frame * 2)
        self.assertEqual(read_ppm(stream), frame)
        self.assertEqual(read_ppm(stream), frame)
        self.assertIsNone(read_ppm(stream))

    def test_partial_pipe_reads(self):
        class PartialStream(io.BytesIO):
            def read(self, size=-1):
                return super().read(min(size, 8192))
        frame = (f"P6\n{PREVIEW_WIDTH} {PREVIEW_HEIGHT}\n255\n".encode()
                 + b"\x00" * (PREVIEW_WIDTH * PREVIEW_HEIGHT * 3))
        self.assertEqual(read_ppm(PartialStream(frame)), frame)

    def test_truncated_preview(self):
        truncated = f"P6\n{PREVIEW_WIDTH} {PREVIEW_HEIGHT}\n255\nabc".encode()
        for data in [b"P6\n", b"P5\n", truncated]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                read_ppm(io.BytesIO(data))


if __name__ == "__main__":
    unittest.main()
