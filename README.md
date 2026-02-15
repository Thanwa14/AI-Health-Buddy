🩺 AI Health Buddy (Strict RAG Version)

แชทบอทให้คำแนะนำสุขภาพเบื้องต้น โดยใช้เทคโนโลยี RAG (Retrieval-Augmented Generation) เพื่อให้ AI ตอบคำถามจากฐานข้อมูลที่กำหนดเท่านั้น ลดการมั่วข้อมูล และไม่ใช้ความรู้ภายนอกระบบ

⚠️ ระบบให้เพียงคำแนะนำเบื้องต้น ไม่ใช่การวินิจฉัยทางการแพทย์

🌟 ฟีเจอร์หลัก

🩺 รับอาการและพูดคุยแบบธรรมชาติ คล้ายเภสัชกร

📚 ตอบจากฐานข้อมูลในระบบเท่านั้น (Strict RAG)

❌ ไม่เดา ไม่วินิจฉัยโรค

💊 แนะนำยาเบื้องต้นเฉพาะเมื่อมีข้อมูลในฐานข้อมูล

🔒 หากไม่มีข้อมูล จะตอบว่า

"ขออภัย ข้อมูลในระบบไม่เพียงพอสำหรับการแนะนำ"

🛠 Tech Stack

Language: Python 3.10+

Framework: Streamlit

LLM: Groq (Model: llama-3.3-70b-versatile)

RAG Framework: LangChain

Vector Database: ChromaDB

Embedding: (ตามที่ตั้งค่าในโปรเจค)

📂 โครงสร้างโปรเจค
AI-Health-Buddy/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env (ไม่ถูก push)
│
└── src/
    ├── chain.py
    ├── prompt.py
    ├── retriever.py
    └── vectorstore.py

⚙️ วิธีติดตั้ง (Local)
1️⃣ Clone โปรเจค
git clone https://github.com/Thanwa14/AI-Health-Buddy.git
cd AI-Health-Buddy

2️⃣ สร้าง Virtual Environment
python -m venv env
env\Scripts\activate   # Windows

3️⃣ ติดตั้ง dependencies
pip install -r requirements.txt

4️⃣ ตั้งค่า API Key

สร้างไฟล์ .env แล้วใส่:

GROQ_API_KEY=your_api_key_here


🔒 ไฟล์ .env จะไม่ถูกอัปโหลดขึ้น GitHub

5️⃣ รันแอป
streamlit run app.py

☁️ Deploy บน Streamlit Cloud

Push โค้ดขึ้น GitHub

ไปที่ https://streamlit.io/cloud

เลือก Repo

ไปที่ Settings → Secrets

เพิ่ม:

GROQ_API_KEY = "your_api_key_here"

🧠 หลักการทำงาน (Strict RAG)

ผู้ใช้พิมพ์อาการ

ระบบค้นหาเอกสารใน Vector Database

LLM จะตอบโดยอิงจาก Context เท่านั้น

หากไม่มีเอกสารที่เกี่ยวข้อง → ระบบจะปฏิเสธการตอบ

⚠️ Disclaimer

ระบบนี้เป็นเพียงเครื่องมือให้คำแนะนำเบื้องต้น
ไม่สามารถแทนที่แพทย์หรือเภสัชกรตัวจริงได้
หากอาการรุนแรง ควรพบแพทย์ทันที
