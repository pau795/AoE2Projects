# Generate a multi-resolution Windows webcam icon using built-in drawing tools.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$sizes = @(16, 24, 32, 48, 64, 128, 256)
$images = @()
foreach ($size in $sizes) {
    $bitmap = [System.Drawing.Bitmap]::new($size, $size)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.ScaleTransform($size / 256.0, $size / 256.0)
    $graphics.Clear([System.Drawing.Color]::Transparent)
    $body = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(45, 55, 72))
    $ring = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(226, 232, 240))
    $lens = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(37, 99, 160))
    $shine = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(186, 230, 253))
    try {
        $graphics.FillRectangle($body, 111, 153, 34, 47)
        $graphics.FillEllipse($body, 54, 185, 148, 42)
        $graphics.FillEllipse($body, 28, 29, 200, 150)
        $graphics.FillEllipse($ring, 74, 50, 108, 108)
        $graphics.FillEllipse($lens, 86, 62, 84, 84)
        $graphics.FillEllipse($body, 105, 81, 46, 46)
        $graphics.FillEllipse($shine, 106, 79, 18, 18)
        $graphics.FillEllipse($shine, 194, 95, 10, 10)
        $stream = [System.IO.MemoryStream]::new()
        try {
            $bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
            $images += ,$stream.ToArray()
        } finally { $stream.Dispose() }
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
        $body.Dispose()
        $ring.Dispose()
        $lens.Dispose()
        $shine.Dispose()
    }
}
$output = [System.IO.File]::Create((Join-Path $PSScriptRoot 'webcam.ico'))
$writer = [System.IO.BinaryWriter]::new($output)
try {
    $writer.Write([uint16]0)
    $writer.Write([uint16]1)
    $writer.Write([uint16]$sizes.Count)
    $offset = 6 + 16 * $sizes.Count
    for ($i = 0; $i -lt $sizes.Count; $i++) {
        $dimension = if ($sizes[$i] -eq 256) { 0 } else { $sizes[$i] }
        $writer.Write([byte]$dimension)
        $writer.Write([byte]$dimension)
        $writer.Write([byte]0)
        $writer.Write([byte]0)
        $writer.Write([uint16]1)
        $writer.Write([uint16]32)
        $writer.Write([uint32]$images[$i].Length)
        $writer.Write([uint32]$offset)
        $offset += $images[$i].Length
    }
    foreach ($data in $images) { $writer.Write([byte[]]$data) }
} finally { $writer.Dispose() }
