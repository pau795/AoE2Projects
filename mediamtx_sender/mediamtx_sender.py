"""Windows webcam publisher for MediaMTX (Python standard library + FFmpeg).

Run: python mediamtx_sender.py
Requires a Windows FFmpeg build with DirectShow and libx264 support. Put
ffmpeg.exe on PATH, beside this script, or select it in the UI. No pip packages
are required. Preview is local and also works without a MediaMTX server.
MediaMTX must allow publishing to the chosen path (default: webcam).
Protocol examples: https://mediamtx.org/docs/publish/ffmpeg
Camera input: https://ffmpeg.org/ffmpeg-devices.html#dshow
"""

from __future__ import annotations

import configparser
import ipaddress
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import BinaryIO, cast
from collections.abc import Iterator
from urllib.parse import quote


ENCODERS = {
    "CPU (x264)": "libx264",
    "NVIDIA GPU (NVENC)": "h264_nvenc",
    "Intel GPU (Quick Sync)": "h264_qsv",
    "AMD GPU (AMF)": "h264_amf",
}
PROTOCOLS = ("RTSP / TCP", "RTSP / UDP", "RTMP")
PREVIEW_WIDTH, PREVIEW_HEIGHT = 480, 270
CREATE_FLAGS = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def application_path() -> Path:
    """Locate persistent files beside the script or the packaged executable."""
    return Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve()


CONFIG_PATH = application_path().with_suffix(".cfg")
DEFAULT_OPTIONS = {
    "ffmpeg": "", "host": "127.0.0.1", "port": "8554", "path": "webcam",
    "protocol": PROTOCOLS[0], "size": "Camera default", "fps": "30",
    "encoder": next(iter(ENCODERS)), "bitrate": "2500", "packet_size": "1200",
    "username": "", "password": "", "remember_password": "false",
    "camera_id": "", "camera_name": "",
}
CHOICES = {
    "protocol": PROTOCOLS, "encoder": tuple(ENCODERS),
    "size": ("Camera default", "640x480", "1280x720", "1920x1080"),
    "fps": ("15", "24", "25", "30", "60"), "remember_password": ("true", "false"),
}


def load_options(path: Path = CONFIG_PATH) -> dict[str, str]:
    options = DEFAULT_OPTIONS.copy()
    parser = configparser.ConfigParser(interpolation=None)
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            parser.read_file(handle)
        if parser.has_section("sender"):
            options.update({key: parser["sender"][key] for key in options if key in parser["sender"]})
    for key, choices in CHOICES.items():
        if options[key] not in choices:
            options[key] = DEFAULT_OPTIONS[key]
    if options["remember_password"] != "true":
        options["password"] = ""
    return options


def save_options(options: dict[str, str], path: Path = CONFIG_PATH) -> None:
    """Atomically replace the config; percent signs and camera paths stay literal."""
    parser = configparser.ConfigParser(interpolation=None)
    saved = {key: options.get(key, default) for key, default in DEFAULT_OPTIONS.items()}
    if saved["remember_password"] != "true":
        saved["password"] = ""
    parser["sender"] = saved
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=path.name + ".", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            parser.write(handle)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def camera_index(devices: list[tuple[str, str]], camera_id: str, camera_name: str) -> int:
    """Prefer a stable device identity even when the discovery order changes."""
    for index, (_, device_id) in enumerate(devices):
        if device_id == camera_id:
            return index
    for index, (name, _) in enumerate(devices):
        if name == camera_name:
            return index
    return 0 if devices else -1


def find_ffmpeg() -> str:
    local = application_path().with_name("ffmpeg.exe")
    return str(local) if local.is_file() else (shutil.which("ffmpeg") or "")


def list_cameras(ffmpeg: str) -> list[tuple[str, str]]:
    """Return friendly labels and unique DirectShow identifiers, including duplicates."""
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=15, creationflags=CREATE_FLAGS,
    )
    # FFmpeg deliberately exits nonzero after listing devices.
    devices: list[tuple[str, str]] = []
    video = False
    for line in result.stderr.splitlines():
        match = re.search(r'"(.*)"\s+\(video\)', line)
        if match:
            name = match.group(1)
            devices.append((name, name))
            video = True
        elif "(audio)" in line:
            video = False
        elif video and devices and "Alternative name" in line:
            alternate = re.search(r'Alternative name "(.*)"', line)
            if alternate:
                devices[-1] = (devices[-1][0], alternate.group(1))
    if not devices and "DirectShow video devices" not in result.stderr:
        # Retain a useful build/driver error instead of reporting no camera.
        if "Unknown input format" in result.stderr:
            raise ValueError("This FFmpeg build does not include Windows DirectShow support.")
    return devices


def destination(host: str, port: str, path: str, protocol: str,
                username: str = "", password: str = "") -> str:
    host, path = host.strip(), path.strip().strip("/")
    if not host or any(c.isspace() for c in host) or any(c in host for c in "/?@#"):
        raise ValueError("Enter a server IP or hostname, without a URL scheme or port.")
    if ":" in host:
        try:
            ipaddress.IPv6Address(host.strip("[]"))
        except ValueError as exc:
            raise ValueError("Enter the port in the Port field; IPv6 addresses are supported.") from exc
        host = f"[{host.strip('[]')}]"
    if not port.isdecimal() or not 1 <= int(port) <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    if not path or any(not segment or segment in (".", "..") for segment in path.split("/")):
        raise ValueError("Enter a stream path, for example webcam or live/webcam.")
    if password and not username:
        raise ValueError("A password requires a username.")
    auth = f"{quote(username, safe='')}:{quote(password, safe='')}@" if username else ""
    scheme = "rtmp" if protocol == "RTMP" else "rtsp"
    return f"{scheme}://{auth}{host}:{port}/{quote(path, safe='/')}"


def build_command(ffmpeg: str, camera: str, size: str, fps: int,
                  encoder: str, bitrate: int, protocol: str,
                  url: str | None = None, packet_size: int = 1200) -> list[str]:
    # New FFmpeg builds accept thread_queue_size only for outputs. Leave input
    # queue management to DirectShow/FFmpeg so old and new builds both work.
    # Keep diagnostic logs while suppressing the repeated progress reports.
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "info", "-nostats", "-nostdin", "-f", "dshow"]
    if size != "Camera default":
        cmd += ["-video_size", size]
    cmd += ["-framerate", str(fps), "-i", f"video={camera}"]
    if url:
        cmd += ["-map", "0:v:0", "-an", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-c:v", encoder, "-pix_fmt", "yuv420p", "-b:v", f"{bitrate}k",
                "-maxrate", f"{bitrate}k", "-bufsize", f"{bitrate * 2}k",
                "-g", str(fps * 2), "-bf", "0"]
        if encoder == "libx264":
            cmd += ["-preset", "veryfast", "-tune", "zerolatency"]
        if protocol == "RTMP":
            cmd += ["-f", "flv", url]
        else:
            if not 256 <= packet_size <= 65507:
                raise ValueError("RTSP packet size must be between 256 and 65507 bytes.")
            cmd += ["-rtsp_transport", "udp" if protocol == "RTSP / UDP" else "tcp",
                    "-pkt_size", str(packet_size), "-f", "rtsp", url]
    # Both outputs use the same open camera. Fixed-size PPM requires no Pillow.
    cmd += ["-map", "0:v:0", "-an", "-vf",
            f"fps=10,scale={PREVIEW_WIDTH}:{PREVIEW_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={PREVIEW_WIDTH}:{PREVIEW_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "ppm", "-pix_fmt", "rgb24", "-f", "image2pipe", "pipe:1"]
    return cmd


def read_log_lines(stream: BinaryIO) -> Iterator[str]:
    """Yield CR/LF-delimited messages without waiting for EOF or a full buffer."""
    read_chunk = getattr(stream, "read1", stream.read)
    pending = b""
    while True:
        chunk = read_chunk(4096)
        if not chunk:
            if pending.strip():
                yield pending.decode("utf-8", errors="replace").strip()
            return
        parts = re.split(rb"[\r\n]", pending + chunk)
        pending = parts.pop()
        for part in parts:
            if part.strip():
                yield part.decode("utf-8", errors="replace").strip()


def read_ppm(stream: BinaryIO) -> bytes | None:
    """Read one binary PPM frame, handling partial pipe reads and clean EOF."""
    magic = stream.readline()
    if not magic:
        return None
    if magic.strip() != b"P6":
        raise ValueError("Unexpected FFmpeg preview format.")
    header = bytearray(magic)
    tokens = []
    while len(tokens) < 3:
        line = stream.readline()
        if not line:
            raise ValueError("Incomplete preview header.")
        header.extend(line)
        tokens.extend(line.split(b"#", 1)[0].split())
    width, height, maximum = map(int, tokens)
    if (width, height, maximum) != (PREVIEW_WIDTH, PREVIEW_HEIGHT, 255):
        raise ValueError("Unexpected preview dimensions.")
    remaining = width * height * 3
    data = bytearray(header)
    while remaining:
        part = stream.read(remaining)
        if not part:
            raise ValueError("Incomplete preview frame.")
        data.extend(part)
        remaining -= len(part)
    return bytes(data)


class SenderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Webcam → MediaMTX")
        if os.name == "nt":
            root.iconbitmap(default=str(Path(__file__).with_name("webcam.ico")))
        root.minsize(800, 660)
        self.events = queue.Queue(maxsize=500)
        self.frames = queue.Queue(maxsize=1)
        self.process: subprocess.Popen | None = None
        self.devices: list[tuple[str, str]] = []
        self.busy = False
        self.closing = False
        self.session = 0
        self.photo = None
        self.save_after = None
        config_error = None
        try:
            options = load_options()
        except (OSError, UnicodeError, configparser.Error) as exc:
            config_error = f"Could not load settings; using defaults: {exc}"
            options = DEFAULT_OPTIONS.copy()
        self.saved_camera_id = options["camera_id"]
        self.saved_camera_name = options["camera_name"]
        options["ffmpeg"] = options["ffmpeg"] or find_ffmpeg()
        self.fields = {key: tk.StringVar(value=value) for key, value in options.items()
                       if key not in ("camera_id", "camera_name")}
        self.fields["camera"] = tk.StringVar()
        body = ttk.Frame(root, padding=12)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(3, weight=1)
        self.settings = []

        def field(row, label, key, values=None, show=None, column=0, span=1):
            ttk.Label(body, text=label).grid(row=row, column=column, sticky="w", pady=3)
            widget = (ttk.Combobox(body, textvariable=self.fields[key], values=values, state="readonly")
                      if values is not None else ttk.Entry(body, textvariable=self.fields[key], show=show))
            widget.grid(row=row, column=column + 1, columnspan=span, sticky="ew", padx=8, pady=3)
            self.settings.append((widget, "readonly" if values is not None else "normal"))
            return widget

        field(0, "FFmpeg executable", "ffmpeg", span=2)
        self.browse = ttk.Button(body, text="Browse…", command=self.browse_ffmpeg)
        self.browse.grid(row=0, column=3)
        self.camera_box = cast(ttk.Combobox, field(1, "Webcam", "camera", [], span=2))
        self.refresh = ttk.Button(body, text="Refresh cameras", command=self.scan)
        self.refresh.grid(row=1, column=3)
        field(2, "Server IP / hostname", "host")
        field(2, "Port", "port", column=2)
        field(3, "Stream path", "path")
        field(3, "Protocol", "protocol", PROTOCOLS, column=2).bind("<<ComboboxSelected>>", self.protocol_changed)
        field(4, "Capture resolution", "size", CHOICES["size"])
        field(4, "Capture FPS", "fps", CHOICES["fps"], column=2)
        field(5, "H.264 encoder", "encoder", list(ENCODERS))
        field(5, "Video bitrate (kbps)", "bitrate", column=2)
        field(6, "Username (optional)", "username")
        field(6, "Password (optional)", "password", show="*", column=2)
        field(7, "RTSP packet bytes", "packet_size")
        remember = ttk.Checkbutton(body, text="Remember password (plaintext in cfg)",
                                   variable=self.fields["remember_password"],
                                   onvalue="true", offvalue="false")
        remember.grid(row=7, column=2, columnspan=2, sticky="w", padx=8)
        self.settings.append((remember, "normal"))
        ttk.Label(body, text="Video only • GPU modes require compatible hardware and FFmpeg support.").grid(
            row=8, column=0, columnspan=4, sticky="w", pady=5)
        buttons = ttk.Frame(body)
        buttons.grid(row=9, column=0, columnspan=4, sticky="w", pady=5)
        self.preview_button = ttk.Button(buttons, text="Preview webcam", command=lambda: self.start(False))
        self.preview_button.pack(side="left", padx=(0, 8))
        self.stream_button = ttk.Button(buttons, text="Start streaming", command=lambda: self.start(True))
        self.stream_button.pack(side="left", padx=8)
        self.stop_button = ttk.Button(buttons, text="Stop", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=8)
        self.status = tk.StringVar(value="Idle")
        ttk.Label(body, textvariable=self.status).grid(row=10, column=0, columnspan=4, sticky="w")
        self.preview = ttk.Label(body, text="Local webcam preview", anchor="center")
        self.preview.grid(row=11, column=0, columnspan=4, sticky="nsew", pady=6)
        self.log = scrolledtext.ScrolledText(body, height=6, state="disabled", wrap="word")
        self.log.grid(row=12, column=0, columnspan=4, sticky="nsew")
        body.rowconfigure(12, weight=1)
        if config_error:
            self.write_log(config_error)
        for variable in self.fields.values():
            variable.trace_add("write", self.schedule_save)
        self.write_log(f"Settings file: {CONFIG_PATH}")
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(50, self.poll)
        if os.name != "nt":
            self.write_log("Camera discovery currently supports Windows (DirectShow) only.")
        elif self.fields["ffmpeg"].get():
            root.after(100, self.scan)
        else:
            self.write_log("Select ffmpeg.exe using Browse, then click Refresh cameras.")

    def schedule_save(self, *_args):
        if self.closing:
            return
        if self.save_after is not None:
            self.root.after_cancel(self.save_after)
        self.save_after = self.root.after(400, self.save_settings)

    def save_settings(self):
        if self.save_after is not None:
            self.root.after_cancel(self.save_after)
            self.save_after = None
        values = {key: variable.get() for key, variable in self.fields.items() if key != "camera"}
        index = self.camera_box.current()
        if 0 <= index < len(self.devices):
            self.saved_camera_name, self.saved_camera_id = self.devices[index]
        values.update(camera_id=self.saved_camera_id, camera_name=self.saved_camera_name)
        try:
            save_options(values)
        except (OSError, ValueError, configparser.Error) as exc:
            self.write_log(f"Could not save settings: {exc}")

    def emit(self, kind, value):
        try:
            self.events.put_nowait((kind, value))
        except queue.Full:
            if kind != "log":
                # Completion events must survive a burst of FFmpeg diagnostic logs.
                self.events.put((kind, value))

    def write_log(self, text):
        # FFmpeg can print the destination URL; redact credentials in every line.
        text = re.sub(r"(rtsp|rtmp)://[^\s/]*@", r"\1://***@", str(text))
        self.log.configure(state="normal")
        self.log.insert("end", f"{time.strftime('%H:%M:%S')}  {text}\n")
        if int(self.log.index("end-1c").split(".")[0]) > 400:
            self.log.delete("1.0", "100.0")
        self.log.see("end")
        self.log.configure(state="disabled")

    def set_busy(self, busy):
        self.busy = busy
        for widget, state in self.settings:
            widget.configure(state="disabled" if busy else state)
        for button in (self.browse, self.refresh, self.preview_button, self.stream_button):
            button.configure(state="disabled" if busy else "normal")
        self.stop_button.configure(state="normal" if self.process is not None else "disabled")

    def browse_ffmpeg(self):
        filename = filedialog.askopenfilename(title="Select FFmpeg executable",
                                              filetypes=[("FFmpeg", "*.exe"), ("All files", "*.*")])
        if filename:
            self.fields["ffmpeg"].set(filename)
            self.scan()

    def executable(self):
        value = self.fields["ffmpeg"].get().strip().strip('"')
        resolved = shutil.which(value)
        if not resolved:
            raise ValueError("FFmpeg was not found. Browse to ffmpeg.exe or add it to PATH.")
        if os.name != "nt":
            raise ValueError("This script currently supports Windows webcams via DirectShow.")
        return resolved

    def protocol_changed(self, _event=None):
        self.fields["port"].set("1935" if self.fields["protocol"].get() == "RTMP" else "8554")

    def scan(self):
        if self.busy:
            return
        try:
            ffmpeg = self.executable()
        except ValueError as exc:
            messagebox.showerror("FFmpeg", str(exc))
            return
        self.set_busy(True)
        self.status.set("Searching for webcams…")

        def worker():
            try:
                self.emit("devices", list_cameras(ffmpeg))
            except (OSError, ValueError, subprocess.TimeoutExpired) as scan_error:
                self.emit("scan_error", str(scan_error))
        threading.Thread(target=worker, daemon=True).start()

    def start(self, streaming):
        if self.busy:
            return
        self.save_settings()
        try:
            ffmpeg = self.executable()
            index = self.camera_box.current()
            if not 0 <= index < len(self.devices):
                raise ValueError("Refresh cameras and select a webcam first.")
            values = {key: variable.get() for key, variable in self.fields.items()}
            fps, bitrate = int(values["fps"]), int(values["bitrate"])
            if not 1 <= bitrate <= 100000:
                raise ValueError("Bitrate must be between 1 and 100000 kbps.")
            url = destination(values["host"], values["port"], values["path"],
                              values["protocol"], values["username"], values["password"]) if streaming else None
            command = build_command(ffmpeg, self.devices[index][1], values["size"], fps,
                                    ENCODERS[values["encoder"]], bitrate, values["protocol"], url,
                                    int(values["packet_size"]) if streaming and values["protocol"] != "RTMP" else 1200)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.DEVNULL, bufsize=0, creationflags=CREATE_FLAGS)
        except (ValueError, OSError) as exc:
            messagebox.showerror("Cannot start", str(exc))
            return
        self.session += 1
        session = self.session
        stdout, stderr = cast(BinaryIO, proc.stdout), cast(BinaryIO, proc.stderr)
        self.process = proc
        self.set_busy(True)
        self.status.set("Starting stream…" if streaming else "Opening webcam…")
        self.write_log(f"Opening {self.devices[index][0]}.")
        if url:
            self.write_log(f"Publishing to {url}")
            if values["protocol"] != "RTMP":
                self.write_log(f"RTSP maximum packet size: {values['packet_size']} bytes.")
        self.write_log("If capture fails, try Camera default, another FPS, or close other camera apps.")

        def frames():
            try:
                while True:
                    frame = read_ppm(stdout)
                    if frame is None:
                        break
                    try:
                        self.frames.get_nowait()
                    except queue.Empty:
                        pass
                    self.frames.put_nowait((session, frame, streaming))
            except (OSError, ValueError) as preview_error:
                if proc.poll() is None:
                    self.emit("log", f"Preview stopped: {preview_error}")
            finally:
                stdout.close()

        def logs():
            for line in read_log_lines(stderr):
                # Some builds still emit terminal statistics despite -nostats.
                # Keep diagnostics live without flooding the UI with progress.
                if re.match(r"^(?:frame\s*=|elapsed\s*=)", line):
                    continue
                self.emit("log", line)
            stderr.close()
            code = proc.wait()
            self.emit("ended", (session, code))
        threading.Thread(target=frames, daemon=True).start()
        threading.Thread(target=logs, daemon=True).start()

    def stop(self):
        proc = self.process
        if proc is None:
            return
        self.status.set("Stopping…")
        self.stop_button.configure(state="disabled")

        def worker():
            assert proc is not None
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            except OSError:
                pass
        threading.Thread(target=worker, daemon=True).start()

    def close(self):
        if self.closing:
            return
        self.save_settings()
        self.closing = True
        if self.process is None:
            self.root.destroy()
        else:
            self.stop()

    def poll(self):
        for _ in range(100):
            try:
                kind, value = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "log":
                self.write_log(value)
            elif kind in ("devices", "scan_error"):
                self.set_busy(False)
                if kind == "devices":
                    old_index = self.camera_box.current()
                    if 0 <= old_index < len(self.devices):
                        self.saved_camera_name, self.saved_camera_id = self.devices[old_index]
                    self.devices = value
                    self.camera_box.configure(values=[f"{i + 1}. {name}" for i, (name, _) in enumerate(value)])
                    if value:
                        self.camera_box.current(camera_index(value, self.saved_camera_id, self.saved_camera_name))
                    else:
                        self.fields["camera"].set("")
                    self.status.set(f"Found {len(value)} webcam(s)")
                    self.write_log(self.status.get())
                else:
                    self.status.set("Camera search failed")
                    self.write_log(value)
            elif kind == "ended" and value[0] == self.session:
                self.process = None
                self.set_busy(False)
                self.status.set(f"Stopped (FFmpeg exit code {value[1]})")
                self.write_log(self.status.get())
                self.preview.configure(image="", text="Local webcam preview")
                self.photo = None
        if self.closing and self.process is None:
            self.root.destroy()
            return
        try:
            session, frame, streaming = self.frames.get_nowait()
            if session == self.session and self.process is not None and not self.closing:
                self.photo = tk.PhotoImage(data=frame, format="PPM")
                self.preview.configure(image=self.photo, text="")
                # A local frame is not proof that the server accepted publication.
                if str(self.stop_button["state"]) != "disabled":
                    self.status.set("Publishing + local preview (see log)" if streaming else "Local preview")
        except queue.Empty:
            pass
        self.root.after(50, self.poll)


def main():
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print(f"Cannot start the UI: {exc}\n"
              "Repair this Python installation with Tcl/Tk support enabled, "
              "then run the script again.", file=sys.stderr)
        return 1
    SenderApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
