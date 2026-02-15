import os
import streamlit as st

def get_api_key():
    # รองรับทั้ง Local (.env) และ Streamlit Cloud (Secrets)
    return os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]
