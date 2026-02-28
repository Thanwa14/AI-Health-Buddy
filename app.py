import os
import gradio as gr
from src.chain import build_chain

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

qa = build_chain(api_key=GROQ_API_KEY)

def respond(message, history):
    try:
        result = qa.invoke({"query": message})
        source_docs = result.get("source_documents")

        if not source_docs:
            answer = "ขออภัย ข้อมูลในระบบไม่เพียงพอสำหรับการแนะนำ"
        else:
            answer = result.get("result") or result.get("answer")

    except Exception as e:
        answer = f"เกิดข้อผิดพลาด: {e}"

    history.append((message, answer))
    return history

with gr.Blocks() as demo:
    gr.Markdown("# 🩺 AI Health Buddy")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="พิมพ์อาการของคุณ...")
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], chatbot)
    clear.click(lambda: [], None, chatbot)

demo.launch(server_name="0.0.0.0", server_port=7860)