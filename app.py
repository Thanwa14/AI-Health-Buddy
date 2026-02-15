import streamlit as st
import os
from dotenv import load_dotenv

# โหลด .env สำหรับ Local
load_dotenv()

# ================== CONFIG ==================
def get_env(key: str):
    """รองรับทั้ง Local (.env) และ Streamlit Cloud (Secrets)"""
    return os.getenv(key) or st.secrets.get(key)

GROQ_API_KEY = get_env("GROQ_API_KEY")

# ================== PAGE ==================
st.set_page_config(
    page_title="AI Health Buddy 🩺",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Health Buddy")

# ================== CHECK API KEY ==================
if not GROQ_API_KEY:
    st.error("❌ ไม่พบ GROQ_API_KEY")
    st.info("👉 ตั้งค่าใน .env หรือ Streamlit Secrets")
    st.stop()

# ================== LOAD CHAIN ==================
@st.cache_resource
def load_chain():
    from src.chain import build_chain
    return build_chain(api_key=GROQ_API_KEY)

if "qa" not in st.session_state:
    try:
        st.session_state.qa = load_chain()
    except Exception as e:
        st.error(f"❌ โหลดระบบไม่สำเร็จ: {e}")
        st.stop()

# ================== SESSION ==================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "สวัสดีครับ 😊 ผมคือ AI Health Buddy\nมีอาการอะไรให้ผมช่วยแนะนำได้บ้างครับ?"
        }
    ]

# แสดงประวัติแชท
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================== INPUT ==================
user_input = st.chat_input("พิมพ์คำถามเกี่ยวกับสุขภาพ...")

if user_input:
    # แสดงข้อความ user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ตอบกลับ
with st.chat_message("assistant"):
    with st.spinner("🧠 กำลังวิเคราะห์อาการ..."):
        try:
            result = st.session_state.qa.invoke({"query": user_input})

            # 🔒 Strict RAG Guard
            source_docs = result.get("source_documents")

            if not source_docs:
                answer = "ขออภัย ข้อมูลในระบบไม่เพียงพอสำหรับการแนะนำ"
            else:
                answer = result.get("result") or result.get("answer")

        except Exception as e:
            answer = f"❌ เกิดข้อผิดพลาด: {e}"

        st.markdown(answer)

st.divider()
st.caption("⚠️ ข้อมูลนี้เป็นเพียงคำแนะนำเบื้องต้น ไม่ใช่การวินิจฉัยทางการแพทย์")
