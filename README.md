🏥🤖 AI Health Buddy
Smart Health Assistant with Strict RAG

แชทบอทให้คำแนะนำสุขภาพเบื้องต้น
พูดคุยเป็นธรรมชาติ คล้ายเภสัชกรตัวจริง
ตอบจากฐานข้อมูลในระบบเท่านั้น ❌ ไม่เดา ❌ ไม่มั่ว

⚠️ ระบบนี้ให้คำแนะนำเบื้องต้นเท่านั้น ไม่ใช่การวินิจฉัยทางการแพทย์

🌟 จุดเด่นของระบบ

✨ พูดคุยแบบธรรมชาติ
ถามอาการเพิ่มก่อนแนะนำ เหมือนคุยกับเภสัชกร

📚 Strict RAG System
AI ตอบจากเอกสารในฐานข้อมูลเท่านั้น
ถ้าไม่มีข้อมูล → จะไม่ตอบมั่ว

💊 แนะนำยาเบื้องต้นอย่างปลอดภัย
แนะนำเฉพาะเมื่อมีข้อมูลอ้างอิงในระบบ

🔒 ควบคุมความปลอดภัยของข้อมูล
ไม่ใช้ความรู้ภายนอก Context

🧠 ระบบทำงานอย่างไร?

1️⃣ ผู้ใช้พิมพ์อาการ
2️⃣ ระบบค้นหาเอกสารใน Vector Database
3️⃣ LLM วิเคราะห์จาก Context เท่านั้น
4️⃣ ถ้าไม่มีข้อมูล → ตอบว่า

"ขออภัย ข้อมูลในระบบไม่เพียงพอสำหรับการแนะนำ"

🛠 Tech Stack

🐍 Python 3.10+

🎈 Streamlit

🧩 LangChain (RAG)

🗂 ChromaDB (Vector Database)

⚡ Groq API (llama-3.3-70b-versatile)
📂 โครงสร้างโปรเจค
AI-Health-Buddy/
│
├── app.py
├── requirements.txt
├── .env (ไม่ถูก push)
│
└── src/
    ├── chain.py
    ├── prompt.py
    ├── retriever.py
    └── vectorstore.py
⚙️ วิธีติดตั้ง (Local)
git clone https://github.com/Thanwa14/AI-Health-Buddy.git
cd AI-Health-Buddy
2️⃣ ติดตั้ง Dependencies
pip install -r requirements.txt
4️⃣ รันแอป
streamlit run app.py
