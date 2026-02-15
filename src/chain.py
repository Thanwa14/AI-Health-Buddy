from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from .vectorstore import load_vectorstore
from .retriever import load_retriever
from .prompt import load_prompt

def build_chain(api_key: str):
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    vectorstore = load_vectorstore()
    retriever = load_retriever(vectorstore)
    prompt = load_prompt()

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
