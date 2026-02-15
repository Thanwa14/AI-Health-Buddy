def load_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_type="mmr",  # ลด hallucination
        search_kwargs={
            "k": 3
        }
    )
