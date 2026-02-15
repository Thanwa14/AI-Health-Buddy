import streamlit as st
from src.chain import build_chain

st.set_page_config(page_title="AI Health Buddy", page_icon="🩺")

st.title("🩺 AI Health Buddy")

if "qa" not in st.session_state:
    st.session_state.qa = build_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงข้อความเก่า
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# รับ input
user_input = st.chat_input("พิมพ์คำถามเกี่ยวกับสุขภาพ...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("กำลังวิเคราะห์..."):
            try:
                result = st.session_state.qa.invoke({"query": user_input})
                answer = result["result"]
            except Exception as e:
                answer = f"❌ Error: {e}"

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.divider()
st.caption("⚠️ ข้อมูลนี้เป็นเพียงคำแนะนำเบื้องต้น ไม่ใช่การวินิจฉัยทางการแพทย์")
