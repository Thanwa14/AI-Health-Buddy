from langchain.vectorstores import Chroma
from .embeddings import load_embeddings

def load_vectorstore():
    return Chroma(
        persist_directory="chroma_db",
        embedding_function=load_embeddings()
    )
