# Cookie Setup Guide - Bypass YouTube Bot Detection

YouTube sometimes requires you to sign in to confirm you're not a bot. This guide explains how to bypass this using cookies.

## Quick Start

The easiest method is to use cookies from your browser:

```bash
python scraper.py --cookies-from-browser chrome -i downloadqueue.txt
```

## Method 1: Extract from Browser (Recommended)

### Prerequisites
- You must be logged into YouTube in the browser
- The browser should be installed on your system

### Supported Browsers
- chrome
- firefox
- edge
- safari (macOS only)
- opera
- brave
- chromium
- vivaldi

### Usage Examples

**Chrome:**
```bash
python scraper.py --cookies-from-browser chrome
```

**Firefox:**
```bash
python scraper.py --cookies-from-browser firefox
```

**Edge:**
```bash
python scraper.py --cookies-from-browser edge
```

**Safari (macOS):**
```bash
python scraper.py --cookies-from-browser safari
```

### Interactive Mode

When running in interactive mode:
```
python scraper.py
```

You'll be prompted:
```
Use cookies to bypass bot detection? [y/N]: y

Cookie options:
  1. Extract from browser (chrome, firefox, edge, safari, etc.)
  2. Use cookies.txt file
Choose option [1]: 1

Available browsers:
  chrome, firefox, edge, safari, opera, brave, chromium
Enter browser name [chrome]: chrome
```

## Method 2: Export Cookies to File

If automatic extraction doesn't work or you prefer manual control:

### Step 1: Install Cookie Export Extension

**Chrome/Edge:**
1. Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

**Firefox:**
1. Install [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

### Step 2: Export Cookies

1. Log into YouTube in your browser
2. Navigate to any YouTube page
3. Click the cookie extension icon
4. Click "Export" or "Download"
5. Save as `cookies.txt` in your project directory

### Step 3: Use the Cookies File

```bash
python scraper.py --cookies cookies.txt -i downloadqueue.txt
```

Or in your download queue directory:
```bash
python scraper.py --cookies /path/to/cookies.txt -i downloadqueue.txt
```

## Troubleshooting

### "Could not find browser" Error
**Solution:** Make sure the browser is installed and accessible. For Chrome on Linux, it might be installed as `google-chrome` or `chromium-browser`.

### "Could not extract cookies" Error
**Solutions:**
1. Close the browser completely and try again
2. Make sure you're logged into YouTube
3. Try a different browser
4. Use Method 2 (manual export) instead

### Still Getting "Sign in to confirm you're not a bot"
**Solutions:**
1. Log out of YouTube and log back in
2. Clear your browser cookies and log in again
3. Export fresh cookies
4. Try a different YouTube account
5. Wait a few hours and try again (you might be temporarily rate-limited)

### Permission Errors (Linux/macOS)
**Solutions:**
1. Close the browser before extracting cookies
2. Check file permissions on the browser's cookie database
3. Run with appropriate permissions (avoid using sudo unless necessary)

### Cookies Expire
YouTube cookies typically last for a while, but they do expire. If downloads start failing again:
1. Re-export fresh cookies
2. Make sure you're still logged into YouTube

## Security Notes

- **Keep cookies private**: Cookie files contain your authentication tokens
- **Don't share cookies**: Anyone with your cookies can access your YouTube account
- **Secure storage**: Store `cookies.txt` files securely and don't commit them to git
- **Regular updates**: Refresh cookies periodically for best results

## Adding cookies.txt to .gitignore

To avoid accidentally committing your cookies:

```bash
echo "cookies.txt" >> .gitignore
```

## Advanced: Using Different Cookie Formats

The scraper supports the Netscape cookie format (the standard for `cookies.txt` files). Make sure your exported cookies are in this format.

## Example Workflow

1. **First time setup:**
   ```bash
   # Log into YouTube in Chrome
   # Then run:
   python scraper.py --cookies-from-browser chrome -i downloadqueue.txt
   ```

2. **If that fails:**
   ```bash
   # Export cookies manually using browser extension
   # Save as cookies.txt
   python scraper.py --cookies cookies.txt -i downloadqueue.txt
   ```

3. **Regular use:**
   ```bash
   # Use the same method that worked for you
   python scraper.py --cookies-from-browser chrome -i downloadqueue.txt
   ```

## Related Documentation

- See [README.md](README.md) for full scraper documentation
- See [EXAMPLES.md](EXAMPLES.md) for more usage examples
- [yt-dlp Cookie Documentation](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
