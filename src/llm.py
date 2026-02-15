import streamlit as st
import os
from langchain_groq import ChatGroq


def load_llm():
    groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found")

    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )
