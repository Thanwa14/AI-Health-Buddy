from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import os

def load_vectorstore():

    persist_directory = "chroma_db"

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ถ้ามี DB อยู่แล้วให้โหลด
    if os.path.exists(persist_directory):
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

    # ถ้าไม่มีให้สร้างใหม่
    loader = TextLoader("data/clean_knowledge.txt")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = text_splitter.split_documents(documents)

    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=persist_directory
    )

    db.persist()

    return db
