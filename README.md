## Requirements
- Python 3.6+
- OS: Windows (can be ran under Wine on macOS & Linux)
- Dolby Reference Player and [FFmpeg binaries](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) in `PATH` environment variable

## Supported Formats
- Dolby Atmos (`.m4a`, `.mp4`, `.ec3`)

## Installation & Usage
1. Copy the files `spatial_audio_tools.ini`, `spatial_audio_tools.py`, and `start.bat` to a folder.
2. Copy any supported spatial audio format files into the same folder.
3. Make any desired configuration changes in the `ini` file and then execute `start.bat` and follow through the printed instructions.

## Credits
- Luna for writing Windows batch scripts that convert Atmos files to WAV and WAV to multiple FLACs
- ScrepTure for helping me test and ensure script works
