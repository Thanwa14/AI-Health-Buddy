import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# ================== CONFIG ==================
def get_env(key: str):
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
    st.stop()

# ================== SESSION ==================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "สวัสดีครับ 😊 ผมคือ AI Health Buddy\nมีอาการอะไรให้ผมช่วยแนะนำได้บ้างครับ?"
        }
    ]

if "qa" not in st.session_state:
    st.session_state.qa = None  # 🔥 ยังไม่โหลดทันที

# ================== SHOW CHAT ==================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================== INPUT ==================
if prompt := st.chat_input("พิมพ์คำถามเกี่ยวกับสุขภาพ..."):

    # แสดงฝั่ง user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 🔥 โหลด chain ครั้งแรกตอนมีคำถาม
    if st.session_state.qa is None:
        with st.spinner("🚀 กำลังเตรียมระบบครั้งแรก..."):
            from src.chain import build_chain
            st.session_state.qa = build_chain(api_key=GROQ_API_KEY)

    # ตอบกลับ
    with st.chat_message("assistant"):
        with st.spinner("🧠 กำลังวิเคราะห์อาการ..."):
            try:
                result = st.session_state.qa.invoke({"query": prompt})

                source_docs = result.get("source_documents")

                if not source_docs:
                    answer = "ขออภัย ข้อมูลในระบบไม่เพียงพอสำหรับการแนะนำ"
                else:
                    answer = result.get("result") or result.get("answer")

            except Exception as e:
                answer = f"❌ เกิดข้อผิดพลาด: {e}"

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
st.caption("⚠️ ข้อมูลนี้เป็นเพียงคำแนะนำเบื้องต้น ไม่ใช่การวินิจฉัยทางการแพทย์")
