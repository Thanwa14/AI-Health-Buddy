from langchain_groq import ChatGroq
from .config import get_api_key

def load_llm():
    return ChatGroq(
        groq_api_key=get_api_key(),
        model_name="llama3-70b-8192",
        temperature=0.3
    )
