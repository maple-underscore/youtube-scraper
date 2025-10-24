# YouTube Video Scraper

A powerful and user-friendly YouTube video downloader with support for multiple formats, codecs, quality options, and tunneling capabilities. Features a beautiful console GUI with progress bars.

## Features

- 📥 **Batch Downloads**: Download multiple videos from a queue file
- 🎬 **Multiple Codecs**: Support for AV1, H.264, H.265, and VP9
- 🎵 **Audio Quality Options**: Choose from 320kbps, 256kbps, 192kbps, 128kbps, and 96kbps
- 📺 **Quality Presets**: 8K, 4K, 1440p, 1080p, 720p, 480p, 360p
- 🔄 **Smart Fallback**: Automatically selects the highest available quality if preferred quality is unavailable
- 🌐 **Proxy Support**: Built-in support for custom proxies and Tor network
- 🎨 **Beautiful UI**: Interactive console interface with progress bars
- ⚡ **Fast & Reliable**: Built on yt-dlp for robust downloading

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (required for merging video and audio)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. Create a `downloadqueue.txt` file with YouTube URLs (one per line):
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=jNQXAC9IVRw
```

2. Run the scraper in interactive mode:
```bash
python scraper.py
```

### Command Line Options

```bash
# Download with custom quality and codec
python scraper.py -q 4k -c av1 -a 320 -i downloadqueue.txt

# Specify output directory
python scraper.py -o /path/to/output -i downloadqueue.txt

# Use Tor for anonymity
python scraper.py --tor -i downloadqueue.txt

# Use custom proxy
python scraper.py --proxy socks5://127.0.0.1:1080 -i downloadqueue.txt

# Force interactive mode
python scraper.py --interactive
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Path to download queue file | `downloadqueue.txt` |
| `-o, --output` | Output directory for downloads | `./downloads` |
| `-q, --quality` | Video quality (8k, 4k, 1440p, 1080p, 720p, 480p, 360p) | `1080p` |
| `-c, --codec` | Video codec (av1, h264, h265, vp9) | `h264` |
| `-a, --audio-bitrate` | Audio bitrate in kbps (320, 256, 192, 128, 96) | `192` |
| `--proxy` | Proxy URL (e.g., socks5://127.0.0.1:1080) | None |
| `--tor` | Use Tor network | False |
| `--interactive` | Run in interactive mode | False |

## Configuration File

You can customize default settings by editing `config.ini`:

```ini
[DEFAULT]
output_dir = ./downloads
quality = 1080p
video_codec = h264
audio_bitrate = 192
queue_file = downloadqueue.txt

[PROXY]
enabled = false
use_tor = false
proxy_url = 

[ADVANCED]
merge_format = mp4
max_concurrent = 1
retry_count = 3
wait_time = 0
```

## Download Queue File Format

The `downloadqueue.txt` file should contain one YouTube URL per line:

```
# You can add comments with #
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2

# Empty lines are ignored
https://www.youtube.com/watch?v=VIDEO_ID_3
```

## Video Codecs

- **AV1**: Modern, efficient codec with excellent compression (requires compatible hardware/software)
- **H.264 (AVC)**: Most compatible, works on all devices
- **H.265 (HEVC)**: Better compression than H.264, newer devices
- **VP9**: Google's open codec, good quality and compression

## Quality Options

The scraper automatically selects the best available quality up to your specified limit:

- **8K**: 7680×4320 (4320p)
- **4K**: 3840×2160 (2160p)
- **1440p**: 2560×1440 (QHD)
- **1080p**: 1920×1080 (Full HD)
- **720p**: 1280×720 (HD)
- **480p**: 854×480 (SD)
- **360p**: 640×360 (Low)

If your selected quality is not available, the scraper will automatically download the highest available quality.

## Proxy & Tunneling

### Using Tor

1. Install and run Tor:
```bash
# Ubuntu/Debian
sudo apt install tor
sudo service tor start

# macOS
brew install tor
tor
```

2. Run scraper with Tor:
```bash
python scraper.py --tor
```

### Using Custom Proxy

```bash
# SOCKS5 proxy
python scraper.py --proxy socks5://127.0.0.1:1080

# HTTP proxy
python scraper.py --proxy http://proxy.example.com:8080

# With authentication
python scraper.py --proxy socks5://user:pass@127.0.0.1:1080
```

## Examples

### Download in highest quality with AV1 codec
```bash
python scraper.py -q 8k -c av1 -a 320
```

### Download 4K videos with high quality audio through Tor
```bash
python scraper.py -q 4k -a 320 --tor
```

### Download to specific directory with custom settings
```bash
python scraper.py -o ~/Videos/YouTube -q 1440p -c h265 -a 256
```

## Troubleshooting

### "FFmpeg not found"
Install FFmpeg as described in the Installation section.

### "No formats found"
The video might not be available in your requested quality/codec. Try a different quality preset or codec.

### Slow downloads
- Try using a different video codec (h264 is usually fastest to encode)
- Lower the quality setting
- Check your internet connection
- Disable proxy if not needed

### Proxy connection failed
- Ensure your proxy/Tor is running
- Check the proxy URL format
- Verify firewall settings

## License

MIT License - Feel free to use and modify as needed.

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [rich](https://github.com/Textualize/rich) - Beautiful terminal formatting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.