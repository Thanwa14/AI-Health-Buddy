import sys
import subprocess
import os

sys.stdout.reconfigure(encoding="utf-8")

def install_package(package):
    """ฟังก์ชันสำหรับติดตั้งแพ็กเกจผ่าน pip"""
    print(f"🔧 กำลังติดตั้ง {package} ...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ ติดตั้ง {package} สำเร็จ!")
    except Exception as e:
        print(f"❌ ติดตั้ง {package} ไม่สำเร็จ: {e}")

print("⏳ กำลังตรวจสอบระบบ...")

required_libs = [
    ("langchain", "langchain.chains"),
    ("langchain-community", "langchain_community"),
    ("langchain-text-splitters", "langchain_text_splitters"),
    ("chromadb", "chromadb"),
]

for package_name, import_name in required_libs:
    try:
        __import__(import_name)
    except ImportError:
        print(f"⚠️ ตรวจพบว่าขาดโปรแกรม: {package_name}")
        install_package(package_name)

try:
    from langchain_community.llms import Ollama
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.document_loaders import TextLoader
    from langchain_community.vectorstores import Chroma
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain_text_splitters import CharacterTextSplitter
except ImportError as e:
    print("\n❌ Import ล้มเหลว")
    print(f"Error: {e}")
    sys.exit()

print("\n🤖 กำลังเตรียมสมอง AI (Llama3)...")
llm = Ollama(model="llama3")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

print("📂 กำลังอ่านไฟล์ข้อมูลยา...")
data_path = "./data/clean_knowledge.txt"

if not os.path.exists(data_path):
    print(f"❌ ไม่พบไฟล์: {data_path}")
    sys.exit()

loader = TextLoader(data_path, encoding="utf-8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
texts = text_splitter.split_documents(documents)
print(f"📊 จำนวน chunk ทั้งหมด: {len(texts)}")

CHROMA_DIR = "./chroma_db"

if os.path.exists(CHROMA_DIR):
    print("⚡ โหลด Vector DB เดิม...")
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
else:
    print("⚙️ กำลังสร้าง Vector DB ครั้งแรก (อาจใช้เวลาหลายนาที)...")
    db = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=CHROMA_DIR
    )
    db.persist()
    print("✅ สร้าง Vector DB สำเร็จ")

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

prompt_template = """
คุณคือ AI Health Buddy เภสัชกรอัจฉริยะ
ใช้ข้อมูลยาจาก Context ด้านล่างนี้ในการแนะนำยา:
{context}

คำถาม: {question}

คำแนะนำ (ตอบเป็นภาษาไทย):
1. ค้นหาชื่อยาที่ "รักษาอาการ" ตรงกับที่ผู้ใช้ถาม
2. บอกชื่อยา, ความแรง, และกลุ่มยา
3. ถ้าเป็นยาอันตราย (Prescription) ให้เตือนว่า "ยาอันตราย ต้องปรึกษาแพทย์/เภสัชกรก่อนซื้อ"
4. ถ้าไม่พบข้อมูลยาที่ตรงกับอาการ ให้ตอบว่า "ขออภัย ไม่พบข้อมูลยาสำหรับอาการนี้ในฐานข้อมูลครับ"

คำตอบ:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)

# ---------------- Loop ----------------
print("\n✅ AI Health Buddy พร้อมทำงานแล้ว! (พิมพ์ 'exit' เพื่อออก)")
print("---------------------------------------------------")

while True:
    query = input("\nบอกอาการมาได้เลย: ")
    if query.lower() == "exit":
        break

    print("🤖 กำลังวิเคราะห์...")
    try:
        result = qa.invoke(query)
        print(f"เภสัชกร AI: {result['result']}")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
