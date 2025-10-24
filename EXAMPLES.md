# YouTube Scraper - Examples

This directory contains example files for the YouTube Video Scraper.

## Example Queue Files

### Standard Quality Downloads (downloadqueue.txt)
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### High Quality Downloads (queue_4k.txt)
For downloading 4K content:
```
# 4K Nature Videos
https://www.youtube.com/watch?v=EXAMPLE_4K_VIDEO_1
https://www.youtube.com/watch?v=EXAMPLE_4K_VIDEO_2
```

### Music Downloads (queue_music.txt)
For downloading music with high audio quality:
```
# Music videos with 320kbps audio
https://www.youtube.com/watch?v=EXAMPLE_MUSIC_1
https://www.youtube.com/watch?v=EXAMPLE_MUSIC_2
```

## Usage Examples

### 1. Basic Usage
Download videos in 1080p with default settings:
```bash
python scraper.py
```

### 2. High Quality 4K Downloads
```bash
python scraper.py -q 4k -c av1 -a 320 -i queue_4k.txt
```

### 3. Fast Downloads (Lower Quality)
```bash
python scraper.py -q 720p -c h264 -a 128
```

### 4. Music Downloads with High Audio Quality
```bash
python scraper.py -q 720p -a 320 -i queue_music.txt
```

### 5. Using Tor for Privacy
```bash
# Make sure Tor is running first
python scraper.py --tor
```

### 6. Using Custom Proxy
```bash
python scraper.py --proxy socks5://127.0.0.1:1080
```

### 7. Custom Output Directory
```bash
python scraper.py -o ~/Videos/YouTube
```

### 8. Maximum Quality Downloads
```bash
python scraper.py -q 8k -c av1 -a 320
```

## Queue File Format

The queue file should contain one YouTube URL per line:

```
# Comments start with #
https://www.youtube.com/watch?v=VIDEO_ID_1

# Empty lines are ignored
https://www.youtube.com/watch?v=VIDEO_ID_2

# You can organize by categories
# === Music Videos ===
https://www.youtube.com/watch?v=MUSIC_VIDEO_1
https://www.youtube.com/watch?v=MUSIC_VIDEO_2

# === Tutorials ===
https://www.youtube.com/watch?v=TUTORIAL_1
```

## Tips

1. **For best compatibility**: Use h264 codec
2. **For best compression**: Use av1 codec (requires modern hardware)
3. **For fast downloads**: Use lower quality presets (720p or lower)
4. **For archival**: Use 4k/8k quality with av1 codec and 320kbps audio
5. **For mobile devices**: Use 720p with h264 codec

## Troubleshooting

If a video fails to download:
- Check if the URL is valid
- Try a different quality preset
- Try a different codec
- Check your internet connection
- Verify FFmpeg is installed
