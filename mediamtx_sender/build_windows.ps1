param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
& $Python -c 'import tkinter; tkinter.Tcl()'
if ($LASTEXITCODE -ne 0) {
    throw 'Tcl/Tk runtime is unavailable. Repair Python or check runtime file access before building.'
}
& $Python -m PyInstaller --version
if ($LASTEXITCODE -ne 0) {
    throw 'PyInstaller is required. Install it with your chosen Python interpreter first.'
}

& $Python -m PyInstaller --noconfirm --onefile --windowed --name mediamtx_sender `
    --icon (Join-Path $PSScriptRoot 'webcam.ico') `
    --add-data "$(Join-Path $PSScriptRoot 'webcam.ico');." `
    --distpath (Join-Path $PSScriptRoot 'dist') `
    --workpath (Join-Path $PSScriptRoot 'build/windows-first') `
    --specpath (Join-Path $PSScriptRoot 'build/windows-first') `
    (Join-Path $PSScriptRoot 'mediamtx_sender.py')
if ($LASTEXITCODE -ne 0) {
    throw 'Executable build failed. See the output above.'
}
Write-Host "Executable: $(Join-Path $PSScriptRoot 'dist/mediamtx_sender.exe')"
Write-Host 'Place ffmpeg.exe beside it, or select FFmpeg using Browse in the app.'
