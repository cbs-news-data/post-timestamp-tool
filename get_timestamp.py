import re
from datetime import datetime, timezone
import instaloader
from zoneinfo import ZoneInfo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        try:
            # Configure headless Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--lang=en-US")

            # Initialize driver
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            # Get fully rendered HTML
            html = driver.page_source
            driver.quit()

            # Extract Unix timestamp
            match = re.search(r'"taken_at":\s?(\d+)', html)
            if not match:
                return None

            timestamp = int(match.group(1))
            dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)

            # Convert to Eastern Time
            dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
            readable = dt_est.strftime('%Y-%m-%d %H:%M:%S %Z')
            return readable

        except Exception as e:
            print(f"Error fetching Instagram timestamp: {e}")
            return None

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
