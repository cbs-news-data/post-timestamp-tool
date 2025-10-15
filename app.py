import streamlit as st
from datetime import datetime, timezone
from get_timestamp import get_insta_timestamp, get_tiktok_timestamp

st.set_page_config(page_title="Post Timestamp Finder", page_icon="🕒")

st.title("When was this posted?")
st.write("Enter an Instagram or TikTok post URL to find out when it was posted.")

url = st.text_input("Post URL", placeholder="https://www.instagram.com/p/ABC123xyz/")

if st.button("Get Timestamp"):
    if not url:
        st.error("Please enter a valid Instagram or TikTok post URL.")
    else:
        with st.spinner("Fetching post timestamp..."):
            if 'instagram' in url:
                try:
                    timestamp = get_insta_timestamp(url)
                except Exception as e:
                    st.error(f"""Error fetching Instagram timestamp. Please try again in a few moments, or follow these steps to extract the timestamp manually:
                             \n1. Copy and paste this into a new browser tab: "view-source:{url}"
                             \n2. Ctrl+F for "taken_at"
                             \n3. Paste the number after "taken_at", called a Unix timestamp, below:
                             """)
                    unix = st.text_input("UNIX Timestamp", placeholder="1697059200")
                    if st.button ("Convert Unix"):
                        if unix:
                            try: 
                                timestamp = datetime.fromtimestamp(int(unix), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                                st.success(f"Post Timestamp: {timestamp}")
                            except ValueError: 
                                st.error("Invalid UNIX timestamp.")
                    timestamp = None
            elif 'tiktok' in url:
                timestamp = get_tiktok_timestamp(url)
            if timestamp:
                st.success(f"Post Timestamp in UTC: {timestamp}")
            else:
                st.error("Could not retrieve the timestamp.")
