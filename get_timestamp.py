import requests
import re
from datetime import datetime, timezone
import instaloader

def get_insta_timestamp(url: str) -> str:
    postid = re.search(r"(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
    if postid:
        postid = postid.group(1)
    else:
        return None
    print(postid)
    L = instaloader.Instaloader(quiet=True)
    post = instaloader.Post.from_shortcode(L.context, postid)
    return post.date_utc

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
    timestamp = int(first_31_bits, 2)

    # 3️⃣ Convert UNIX timestamp to human-readable date
    readable = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    return readable