# Webcam sender for MediaMTX

A Windows desktop UI that lists DirectShow webcam devices, previews the selected
camera locally, and publishes H.264 video to a MediaMTX server. Video only.
Uses Python's standard library; no pip packages are needed.

## Requirements and launch

1. Python with working Tkinter / Tcl/Tk support.
2. A Windows [FFmpeg build](https://ffmpeg.org/download.html) with DirectShow and
   `libx264` support. Optional GPU encoders also depend on the build and hardware.
3. A reachable MediaMTX server allowing publication to your chosen stream path.

Run from the project root:

```powershell
python mediamtx_sender/mediamtx_sender.py
```

If `python` resolves to a broken Windows app alias, use the full interpreter
path. For the global interpreter currently on this PC:

```powershell
& 'C:/Users/pau_7/AppData/Local/Python/pythoncore-3.14-64/python.exe' mediamtx_sender/mediamtx_sender.py
```

Select `ffmpeg.exe` with **Browse**, put it next to the script, or add its directory
to PATH. Click **Refresh cameras**, select a webcam, and use **Preview webcam**.
Click **Stop** before changing settings or switching from preview to publishing.
Preview does not require a running server. While publishing, the same camera
capture also supplies the preview.

Enter the server IP or hostname, port, and path, then click **Start streaming**.
The host field accepts IPv4, IPv6, and hostnames; enter the port separately.
Credentials are optional and hidden from the log. The local preview alone does not confirm server acceptance; inspect
the log and open the stream with a client to verify publication.

## Windows executable

Build on Windows with Python and PyInstaller installed:

```powershell
./mediamtx_sender/build_windows.ps1 -Python 'C:/Users/pau_7/AppData/Local/Python/pythoncore-3.14-64/python.exe'
```

The output is `mediamtx_sender/dist/mediamtx_sender.exe`. Copy it to a writable
folder on the destination Windows PC. Python and Tkinter are included; Python
does not need to be installed there. FFmpeg is separate: place a Windows
`ffmpeg.exe` beside the executable, or select an installed copy using Browse.
Use a compatible FFmpeg build and drivers for GPU encoding.

Settings are saved to `mediamtx_sender.cfg` beside the executable and survive
restarts. The build does not include your existing settings or credentials.
The executable architecture follows the Python interpreter used to build it.

## Saved options

Options are automatically saved to `mediamtx_sender.cfg` beside the script,
shortly after edits and when starting a capture or closing the window. The next
launch restores FFmpeg's path, server details, capture/encoder settings, packet
size, username, and webcam selection. Cameras are matched by device identity
first, then by name, so a changed discovery order does not select another camera.
If the saved camera is unavailable, the first available camera is selected.

Passwords are saved only if **Remember password (plaintext in cfg)** is checked.
Unchecking it removes the saved password. The configuration is ignored by Git.
You can edit the INI-style `[sender]` section while the app is closed; percent
signs and Windows paths are treated literally. Missing values use defaults,
and an unreadable/malformed file is reported in the log instead of blocking launch.
Closing the app replaces the configuration with the latest options.

## Server and playback

The defaults publish to `rtsp://SERVER_IP:8554/webcam` over TCP. Open that URL in
VLC or another RTSP client. The alternative RTMP default is
`rtmp://SERVER_IP:1935/webcam`. MediaMTX supports both forms of publication; see
its [FFmpeg documentation](https://mediamtx.org/docs/publish/ffmpeg).

A server with default publisher paths is sufficient. For an explicit path,
merge this into the server's existing `mediamtx.yml`:

```yaml
paths:
  webcam:
    source: publisher
```

Allow the chosen protocol through the server firewall. RTSP TCP uses the RTSP
port; RTSP UDP additionally requires the server's configured RTP/RTCP UDP ports.
Authentication and port changes must match your server's configuration.

The RTSP sender limits packets to **1200 bytes** by default (`-pkt_size 1200`),
for both TCP and UDP. Adjust **RTSP packet bytes** if needed; this option does
not apply to RTMP or local preview. Keep it below the server/network limit.
MediaMTX's `RTP packets are too big (1460 > 1440), remuxing them into smaller ones`
message means it is automatically repacketizing incoming RTP; it does not prevent
streaming or require video re-encoding. Limiting packet size at the sender avoids
that extra repacketization. See the [maintainer's explanation](https://github.com/bluenviron/mediamtx/discussions/5897)
and [FFmpeg's RTSP packet-size option](https://ffmpeg.org/ffmpeg-protocols.html#Muxer).

## Troubleshooting

- Missing `init.tcl` or failure creating the UI: repair/reinstall Python with
  Tcl/Tk support. Importing `tkinter` alone does not verify the runtime files.
- Empty webcam list: check Windows camera privacy permissions, USB connections,
  and that FFmpeg includes DirectShow. Refresh after plugging in a camera.
- Camera fails to open: close applications using it. Try **Camera default** and
  another capture FPS; not every camera supports every resolution/FPS pair.
- GPU initialization failure: select **CPU (x264)** or check the GPU driver and
  whether FFmpeg includes the selected encoder. The app does not silently switch
  encoders.
- Publication fails: inspect the log for authentication, unreachable host,
  rejected path, or codec errors. Test RTSP over TCP first.

The UI remains responsive during device discovery and streaming. **Stop** and
closing the window terminate the owned FFmpeg process. Camera names with the
same friendly label are distinguished using DirectShow alternative identifiers.
FFmpeg's repeated `frame=... fps=... elapsed=...` progress reports are disabled.
Startup messages, warnings, and errors still appear as they are emitted, without
accumulating carriage-return progress text until streaming stops.
The log reader handles both carriage returns and newlines, and reads available
pipe data without waiting for a full buffer or process termination.

Run the standard-library checks from the project root:

```powershell
python -m unittest discover -s mediamtx_sender -p 'test_*.py' -v
```
