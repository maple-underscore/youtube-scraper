#!/usr/bin/env python3
"""
YouTube Video Scraper
A powerful YouTube video downloader with multiple format and quality options.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import yt_dlp
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    DownloadColumn,
)
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt, Confirm

console = Console()

# Quality presets mapping
QUALITY_PRESETS = {
    '8k': 'bestvideo[height<=4320]+bestaudio',
    '4k': 'bestvideo[height<=2160]+bestaudio',
    '1440p': 'bestvideo[height<=1440]+bestaudio',
    '1080p': 'bestvideo[height<=1080]+bestaudio',
    '720p': 'bestvideo[height<=720]+bestaudio',
    '480p': 'bestvideo[height<=480]+bestaudio',
    '360p': 'bestvideo[height<=360]+bestaudio',
}

# Video codec mapping
VIDEO_CODECS = {
    'av1': 'av01',
    'h264': 'avc1',
    'h265': 'hev1',
    'vp9': 'vp9',
}

# Audio bitrate presets (in kbps)
AUDIO_BITRATES = ['320', '256', '192', '128', '96']


class YouTubeScraper:
    """Main YouTube scraper class."""
    
    def __init__(
        self,
        output_dir: str = './downloads',
        quality: str = '1080p',
        video_codec: str = 'h264',
        audio_bitrate: str = '192',
        proxy: Optional[str] = None,
        use_tor: bool = False,
        cookies_from_browser: Optional[str] = None,
        cookies_file: Optional[str] = None,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.video_codec = video_codec
        self.audio_bitrate = audio_bitrate
        self.proxy = proxy
        self.use_tor = use_tor
        self.cookies_from_browser = cookies_from_browser
        self.cookies_file = cookies_file
        self.progress = None
        self.task = None
        
    def _get_format_string(self) -> str:
        """Build the format string for yt-dlp based on quality and codec preferences."""
        # Start with quality preset
        base_format = QUALITY_PRESETS.get(self.quality, QUALITY_PRESETS['1080p'])
        
        # Add codec preference if specified
        if self.video_codec in VIDEO_CODECS:
            codec = VIDEO_CODECS[self.video_codec]
            # Prefer the specified codec, but fallback to best if not available
            format_str = f'bestvideo[vcodec^={codec}][height<={self._get_height()}]+bestaudio/bestvideo[height<={self._get_height()}]+bestaudio/best'
        else:
            # Use quality-based format with fallback to best
            format_str = f'{base_format}/best'
            
        return format_str
    
    def _get_height(self) -> int:
        """Get maximum height from quality preset."""
        height_map = {
            '8k': 4320,
            '4k': 2160,
            '1440p': 1440,
            '1080p': 1080,
            '720p': 720,
            '480p': 480,
            '360p': 360,
        }
        return height_map.get(self.quality, 1080)
    
    def _progress_hook(self, d: Dict):
        """Hook for yt-dlp to update progress bar."""
        if d['status'] == 'downloading':
            if self.progress and self.task is not None:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    self.progress.update(
                        self.task,
                        total=total,
                        completed=downloaded,
                    )
        elif d['status'] == 'finished':
            if self.progress and self.task is not None:
                self.progress.update(self.task, completed=d.get('total_bytes', 0))
    
    def _get_ydl_opts(self, url: str) -> Dict:
        """Build yt-dlp options dictionary."""
        opts = {
            'format': self._get_format_string(),
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',  # Merge to mp4 container
            'quiet': True,
            'no_warnings': True,
            'no_color': True,  # Disable ANSI color codes in output
        }
        
        # Add audio quality postprocessor for better audio
        # We don't extract audio, just ensure good audio quality in the merged file
        opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
        
        # Set audio quality in format string (handled by format selection)
        
        # Add proxy settings
        if self.proxy:
            opts['proxy'] = self.proxy
        elif self.use_tor:
            opts['proxy'] = 'socks5://127.0.0.1:9050'
        
        # Add cookie settings to bypass bot detection
        if self.cookies_from_browser:
            opts['cookiesfrombrowser'] = (self.cookies_from_browser,)
        elif self.cookies_file:
            opts['cookiefile'] = self.cookies_file
        
        return opts
    
    def download_video(self, url: str) -> bool:
        """Download a single video."""
        try:
            ydl_opts = self._get_ydl_opts(url)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                
                console.print(f"\n[cyan]Downloading:[/cyan] {title}")
                
                # Create progress bar for this download
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    DownloadColumn(),
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    self.progress = progress
                    self.task = progress.add_task(
                        f"[green]Downloading {title[:50]}...",
                        total=100
                    )
                    
                    # Download the video
                    ydl.download([url])
                    
                console.print(f"[green]✓[/green] Successfully downloaded: {title}")
                return True
                
        except Exception as e:
            console.print(f"[red]✗[/red] Error downloading {url}: {str(e)}")
            return False
        finally:
            self.progress = None
            self.task = None
    
    def download_from_queue(self, queue_file: str) -> tuple[int, int]:
        """Download all videos from a queue file."""
        queue_path = Path(queue_file)
        
        if not queue_path.exists():
            console.print(f"[red]Error:[/red] Queue file '{queue_file}' not found.")
            return 0, 0
        
        # Read URLs from file
        with open(queue_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            console.print("[yellow]Warning:[/yellow] No URLs found in queue file.")
            return 0, 0
        
        console.print(f"\n[bold]Found {len(urls)} video(s) in queue[/bold]")
        
        # Download each video
        success_count = 0
        fail_count = 0
        
        for i, url in enumerate(urls, 1):
            console.print(f"\n[bold cyan]Video {i}/{len(urls)}[/bold cyan]")
            if self.download_video(url):
                success_count += 1
            else:
                fail_count += 1
        
        return success_count, fail_count


def show_banner():
    """Display welcome banner."""
    banner = """
[bold cyan]╔══════════════════════════════════════════════════════════╗
║                                                          ║
║            YouTube Video Scraper v1.0                    ║
║        Download videos in multiple formats & quality     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝[/bold cyan]
    """
    console.print(banner)


def show_config_summary(config: Dict):
    """Display configuration summary."""
    table = Table(title="Download Configuration", box=box.ROUNDED)
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    
    table.add_row("Quality", config['quality'])
    table.add_row("Video Codec", config['video_codec'])
    table.add_row("Audio Bitrate", f"{config['audio_bitrate']} kbps")
    table.add_row("Output Directory", config['output_dir'])
    
    if config.get('proxy'):
        table.add_row("Proxy", config['proxy'])
    elif config.get('use_tor'):
        table.add_row("Proxy", "Tor (socks5://127.0.0.1:9050)")
    else:
        table.add_row("Proxy", "None")
    
    if config.get('cookies_from_browser'):
        table.add_row("Cookies", f"From browser: {config['cookies_from_browser']}")
    elif config.get('cookies_file'):
        table.add_row("Cookies", f"From file: {config['cookies_file']}")
    else:
        table.add_row("Cookies", "None")
    
    console.print("\n")
    console.print(table)
    console.print("\n")


def interactive_mode():
    """Run in interactive mode with user prompts."""
    show_banner()
    
    console.print("[bold]Welcome to Interactive Mode![/bold]\n")
    
    # Get queue file
    queue_file = Prompt.ask(
        "Enter path to download queue file",
        default="downloadqueue.txt"
    )
    
    # Get quality
    console.print("\n[bold]Available quality options:[/bold]")
    console.print("  8k, 4k, 1440p, 1080p, 720p, 480p, 360p")
    quality = Prompt.ask(
        "Select quality",
        default="1080p",
        choices=['8k', '4k', '1440p', '1080p', '720p', '480p', '360p']
    )
    
    # Get video codec
    console.print("\n[bold]Available video codecs:[/bold]")
    console.print("  av1, h264, h265, vp9")
    video_codec = Prompt.ask(
        "Select video codec",
        default="h264",
        choices=['av1', 'h264', 'h265', 'vp9']
    )
    
    # Get audio bitrate
    console.print("\n[bold]Available audio bitrates:[/bold]")
    console.print("  320, 256, 192, 128, 96 (kbps)")
    audio_bitrate = Prompt.ask(
        "Select audio bitrate",
        default="192",
        choices=AUDIO_BITRATES
    )
    
    # Get output directory
    output_dir = Prompt.ask(
        "Enter output directory",
        default="./downloads"
    )
    
    # Proxy settings
    use_proxy = Confirm.ask("Use proxy/tunneling?", default=False)
    proxy = None
    use_tor = False
    
    if use_proxy:
        use_tor = Confirm.ask("Use Tor (socks5://127.0.0.1:9050)?", default=False)
        if not use_tor:
            proxy = Prompt.ask("Enter proxy URL (e.g., socks5://127.0.0.1:1080)")
    
    # Cookie settings for bot detection bypass
    cookies_from_browser = None
    cookies_file = None
    
    use_cookies = Confirm.ask("Use cookies to bypass bot detection?", default=False)
    if use_cookies:
        console.print("\n[bold]Cookie options:[/bold]")
        console.print("  1. Extract from browser (chrome, firefox, edge, safari, etc.)")
        console.print("  2. Use cookies.txt file")
        cookie_choice = Prompt.ask("Choose option", choices=['1', '2'], default='1')
        
        if cookie_choice == '1':
            console.print("\n[bold]Available browsers:[/bold]")
            console.print("  chrome, firefox, edge, safari, opera, brave, chromium")
            cookies_from_browser = Prompt.ask(
                "Enter browser name",
                default="chrome"
            )
        else:
            cookies_file = Prompt.ask(
                "Enter path to cookies.txt file",
                default="cookies.txt"
            )
    
    # Show configuration
    config = {
        'quality': quality,
        'video_codec': video_codec,
        'audio_bitrate': audio_bitrate,
        'output_dir': output_dir,
        'proxy': proxy,
        'use_tor': use_tor,
        'cookies_from_browser': cookies_from_browser,
        'cookies_file': cookies_file,
    }
    
    show_config_summary(config)
    
    # Confirm and start
    if Confirm.ask("Start downloading?", default=True):
        scraper = YouTubeScraper(
            output_dir=output_dir,
            quality=quality,
            video_codec=video_codec,
            audio_bitrate=audio_bitrate,
            proxy=proxy,
            use_tor=use_tor,
            cookies_from_browser=cookies_from_browser,
            cookies_file=cookies_file,
        )
        
        success, failed = scraper.download_from_queue(queue_file)
        
        # Show summary
        console.print("\n")
        console.print(Panel(
            f"[bold]Download Complete![/bold]\n\n"
            f"[green]✓ Successful:[/green] {success}\n"
            f"[red]✗ Failed:[/red] {failed}\n"
            f"[cyan]Output:[/cyan] {output_dir}",
            title="Summary",
            border_style="green"
        ))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='YouTube Video Scraper - Download videos with multiple format options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python scraper.py

  # Download with custom settings
  python scraper.py -q 4k -c av1 -a 320 -i downloadqueue.txt

  # Use Tor for anonymity
  python scraper.py --tor -i downloadqueue.txt

  # Use custom proxy
  python scraper.py --proxy socks5://127.0.0.1:1080 -i downloadqueue.txt
  
  # Extract cookies from Chrome to bypass bot detection
  python scraper.py --cookies-from-browser chrome -i downloadqueue.txt
  
  # Use cookies.txt file
  python scraper.py --cookies cookies.txt -i downloadqueue.txt
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        help='Path to download queue file (default: downloadqueue.txt)',
        default='downloadqueue.txt'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory for downloads (default: ./downloads)',
        default='./downloads'
    )
    
    parser.add_argument(
        '-q', '--quality',
        help='Video quality preset',
        choices=['8k', '4k', '1440p', '1080p', '720p', '480p', '360p'],
        default='1080p'
    )
    
    parser.add_argument(
        '-c', '--codec',
        help='Preferred video codec',
        choices=['av1', 'h264', 'h265', 'vp9'],
        default='h264'
    )
    
    parser.add_argument(
        '-a', '--audio-bitrate',
        help='Audio bitrate in kbps',
        choices=AUDIO_BITRATES,
        default='192'
    )
    
    parser.add_argument(
        '--proxy',
        help='Proxy URL (e.g., socks5://127.0.0.1:1080)',
        default=None
    )
    
    parser.add_argument(
        '--tor',
        help='Use Tor network (socks5://127.0.0.1:9050)',
        action='store_true'
    )
    
    parser.add_argument(
        '--cookies-from-browser',
        help='Extract cookies from browser (chrome, firefox, edge, safari, etc.)',
        default=None
    )
    
    parser.add_argument(
        '--cookies',
        help='Path to cookies.txt file',
        default=None
    )
    
    parser.add_argument(
        '--interactive',
        help='Run in interactive mode',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Run interactive mode if requested or if no queue file specified
    if args.interactive or (len(sys.argv) == 1):
        interactive_mode()
    else:
        show_banner()
        
        config = {
            'quality': args.quality,
            'video_codec': args.codec,
            'audio_bitrate': args.audio_bitrate,
            'output_dir': args.output,
            'proxy': args.proxy,
            'use_tor': args.tor,
            'cookies_from_browser': args.cookies_from_browser,
            'cookies_file': args.cookies,
        }
        
        show_config_summary(config)
        
        scraper = YouTubeScraper(
            output_dir=args.output,
            quality=args.quality,
            video_codec=args.codec,
            audio_bitrate=args.audio_bitrate,
            proxy=args.proxy,
            use_tor=args.tor,
            cookies_from_browser=args.cookies_from_browser,
            cookies_file=args.cookies,
        )
        
        success, failed = scraper.download_from_queue(args.input)
        
        console.print("\n")
        console.print(Panel(
            f"[bold]Download Complete![/bold]\n\n"
            f"[green]✓ Successful:[/green] {success}\n"
            f"[red]✗ Failed:[/red] {failed}\n"
            f"[cyan]Output:[/cyan] {args.output}",
            title="Summary",
            border_style="green"
        ))


if __name__ == '__main__':
    main()
