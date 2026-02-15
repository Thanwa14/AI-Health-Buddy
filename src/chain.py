from langchain.chains import RetrievalQA
from .llm import load_llm
from .vectorstore import load_vectorstore
from .retriever import load_retriever
from .prompt import load_prompt

def build_chain():
    llm = load_llm()
    vectorstore = load_vectorstore()
    retriever = load_retriever(vectorstore)
    prompt = load_prompt()

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
