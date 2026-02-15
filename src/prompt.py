from langchain.prompts import PromptTemplate

def load_prompt():
    template = """
คุณคือ AI Health Assistant
ตอบตามข้อมูลเท่านั้น

Context:
{context}

Question:
{question}

Answer:
"""
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
