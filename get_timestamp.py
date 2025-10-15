import requests
import re
from datetime import datetime, timezone
import instaloader
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright

def get_insta_timestamp(url: str) -> str:
    try: 
        postid = re.search(r"(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
        if postid:
            postid = postid.group(1)
            L = instaloader.Instaloader(quiet=True)
            post = instaloader.Post.from_shortcode(L.context, postid)
            timestamp = post.date_utc
            readable = timestamp.astimezone(ZoneInfo("America/New_York")).strftime('%Y-%m-%d %H:%M:%S %Z')
            return readable
    except:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # headless browser
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            html = page.content()
            browser.close()
            match = re.search(r'"taken_at":\s?(\d+)', html)
            if not match:
                return None
            timestamp = datetime.fromtimestamp(int(match.group(1)), tz=timezone.utc)
            readable = timestamp.astimezone(ZoneInfo("America/New_York")).strftime('%Y-%m-%d %H:%M:%S %Z')
            return readable

def get_tiktok_timestamp(url: str) -> str:
    match = re.search(r"/video/(\d+)", url)
    if match:
        vid_id = match.group(1)
    else:
        return None
    
    # TikTok IDs are 64-bit integers; first 31 bits encode the upload time
    vid_id_int = int(vid_id)
    as_binary = bin(vid_id_int)[2:]  # Convert to binary string, remove '0b'
    first_31_bits = as_binary[:31]   # First 31 bits
    unix = int(first_31_bits, 2)
    timestamp = datetime.fromtimestamp(unix, tz=timezone.utc)
    readable = timestamp.astimezone(ZoneInfo("America/New_York")).strftime('%Y-%m-%d %H:%M:%S %Z')
    return readable
