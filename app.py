import streamlit as st
from get_timestamp import get_insta_timestamp, get_tiktok_timestamp

st.set_page_config(page_title="Post Timestamp Finder", page_icon="🕒")

st.title("When was this posted?")
st.write("Enter an Instagram or TikTok post URL to find out when it was posted.")

url = st.text_input("Post URL", placeholder="https://www.instagram.com/p/ABC123xyz/")

if st.button("Get Timestamp"):
    if not url:
        st.error("Please enter a valid Instagram or TikTok post URL.")
    else:
        try:
            if 'instagram' in url:
                timestamp = get_insta_timestamp(url)
            elif 'tiktok' in url:
                timestamp = get_tiktok_timestamp(url)
            if timestamp:
                st.success(f"Post Timestamp in UTC: {timestamp}")
            else:
                st.error("Could not retrieve the timestamp.")

        except Exception as e:
            st.error(f"Network error: {e}")