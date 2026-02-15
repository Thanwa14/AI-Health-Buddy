import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI Health Buddy 🩺",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Health Buddy")
st.caption("เภสัชกรอัจฉริยะ (Groq • RAG • Chat)")

# ================== LOAD API KEY ==================
groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not groq_api_key:
    st.error("❌ ไม่พบ GROQ_API_KEY กรุณาใส่ใน Streamlit Secrets")
    st.stop()

# ================== PROMPT ==================
prompt_template = """
คุณคือ "AI Health Buddy" ซึ่งเป็นเภสัชกรที่สุภาพ เป็นมิตร และเข้าใจผู้ป่วย

กติกา:
- ใช้ข้อมูลจาก Context เท่านั้น
- ห้ามเดาข้อมูลที่ไม่มี
- ตอบเป็นภาษาไทยแบบธรรมชาติ
- ตอบต่อเนื่องจากบทสนทนา
- ถ้าเป็นยาอันตรายให้เตือนอย่างสุภาพ
- หลังตอบ ต้องถามกลับอย่างน้อย 1 คำถาม

Context:
{context}

คำถามผู้ใช้:
{question}

คำตอบ:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# ================== LOAD SYSTEM ==================
@st.cache_resource
def load_system():

    # LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # โหลดไฟล์ knowledge
    loader = TextLoader("data/clean_knowledge.txt", encoding="utf-8")
    documents = loader.load()

    # แบ่งข้อความ
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)

    # สร้าง Vector DB แบบ runtime
    db = Chroma.from_documents(
        texts,
        embeddings
    )

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


qa = load_system()

# ================== SESSION STATE ==================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "สวัสดีครับ 😊 ผมคือ AI Health Buddy\nมีอาการอะไรให้ผมช่วยแนะนำได้บ้างครับ?"
        }
    ]

# ================== SHOW CHAT ==================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================== INPUT ==================
user_input = st.chat_input("พิมพ์อาการของคุณที่นี่...")

if user_input:
    # แสดงข้อความ user
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # ตอบกลับ
    with st.chat_message("assistant"):
        with st.spinner("🧠 กำลังวิเคราะห์อาการ..."):
            try:
                result = qa.invoke({"question": user_input})
                ai_reply = result["answer"]
            except Exception as e:
                ai_reply = f"❌ เกิดข้อผิดพลาด: {e}"

            st.markdown(ai_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

st.divider()
st.caption("⚠️ ข้อมูลนี้เป็นเพียงคำแนะนำเบื้องต้น ไม่ใช่การวินิจฉัยทางการแพทย์")
