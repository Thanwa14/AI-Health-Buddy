import streamlit as st
from src.chain import build_chain

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI Health Buddy 🩺",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Health Buddy")
st.caption("เภสัชกรอัจฉริยะ (Groq • RAG • Chat)")

# ================== LOAD SYSTEM ==================
try:
    qa = build_chain()
except Exception as e:
    st.error(f"❌ System error: {e}")
    st.stop()

# ================== SESSION ==================
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
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

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
