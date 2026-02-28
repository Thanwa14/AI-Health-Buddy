import pandas as pd
import os

# ตั้งค่าชื่อไฟล์
INPUT_FILE = "./data/medicine_dataset.csv"   # ไฟล์ CSV ของคุณ
OUTPUT_FILE = "./data/clean_knowledge.txt"   # ไฟล์ที่จะส่งให้ AI

print(f"🔄 กำลังอ่านไฟล์: {INPUT_FILE}")

try:
    df = pd.read_csv(INPUT_FILE)
    
    useful_cols = ['Name', 'Category', 'Indication', 'Classification', 'Strength', 'Dosage Form']
    df_clean = df[useful_cols].dropna()

    print("🧹 กำลังแปลงข้อมูล...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        count = 0
        for index, row in df_clean.iterrows():
            text_chunk = f"""
ชื่อยา: {row['Name']}
กลุ่มยา: {row['Category']}
สรรพคุณ: {row['Indication']}
รูปแบบ: {row['Dosage Form']} ({row['Strength']})
ประเภท: {row['Classification']}
--------------------------------------------------
"""
            f.write(text_chunk)
            count += 1
            
    print(f"✅ สำเร็จ! แปลงข้อมูล {count} รายการ เรียบร้อย")
    print(f"📄 บันทึกไฟล์ไว้ที่: {OUTPUT_FILE}")

except Exception as e:
    print(f"❌ Error: {e}")