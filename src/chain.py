from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from src.llm import load_llm
from src.vectorstore import load_vectorstore
from src.prompt import PROMPT


def build_chain():
    llm = load_llm()
    db = load_vectorstore()

    retriever = db.as_retriever(search_kwargs={"k": 2})

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )

    return qa_chain
