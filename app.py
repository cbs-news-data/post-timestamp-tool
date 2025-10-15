import streamlit as st
from datetime import datetime, timezone
from get_timestamp import get_insta_timestamp, get_tiktok_timestamp

st.set_page_config(page_title="Post Timestamp Finder", page_icon="🕒")

st.title("When was this posted?")
st.write("Enter an Instagram or TikTok post URL to find out when it was posted.")

url = st.text_input("Post URL", placeholder="https://www.instagram.com/p/ABC123xyz/")

st.session_state.clear()
if 'timestamp' not in st.session_state:
    st.session_state.timestamp = None
if 'unix' not in st.session_state:
    st.session_state.unix = ''
if 'platform' not in st.session_state:
    st.session_state.platform = ''

if st.button("Get Timestamp"):
    if not url:
        st.error("Please enter a valid Instagram or TikTok post URL.")
    else:
        with st.spinner("Fetching post timestamp..."):
            if 'instagram' in url:
                st.session_state.platform = 'instagram'
                try:
                    st.session_state.timestamp = get_insta_timestamp(url)
                except Exception as e:
                    st.error(f"""Error fetching Instagram timestamp. Please try again in a few moments, or follow these steps to extract the timestamp manually:
                             \n1. Copy and paste this into a new browser tab: "view-source:{url}"
                             \n2. Ctrl+F for "taken_at"
                             \n3. Paste the number after "taken_at", called a Unix timestamp, below:
                             """)
            elif 'tiktok' in url:
                st.session_state.platform = 'tiktok'
                st.session_state.timestamp = get_tiktok_timestamp(url)

if st.session_state.timestamp is None and st.session_state.platform == 'instagram':
    st.session_state.unix = st.text_input("UNIX Timestamp", value=st.session_state.unix, placeholder="1697059200")
    if st.button("Convert Unix"):
        try:
            st.session_state.timestamp = datetime.fromtimestamp(int(st.session_state.unix), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        except ValueError:
            st.error("Invalid UNIX timestamp.")

if st.session_state.timestamp:
    st.success(f"Post Timestamp: {st.session_state.timestamp}")
