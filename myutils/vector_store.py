# myutils/vector_store.py

import os
import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "vector_db/chroma_store"

def get_vector_store(persist_directory=CHROMA_DIR):
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectordb

def load_questions_from_json(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return questions

def store_questions_to_vector_db(questions, persist_directory=CHROMA_DIR):
    # 📂 Accept either a path or list of dicts
    if isinstance(questions, str):
        questions = load_questions_from_json(questions)

    # 🧹 Ensure list
    if not isinstance(questions, list):
        raise ValueError("Expected a list of questions or a JSON file path.")

    docs = []
    for q in questions:
        content = q.get("question_text", "")
        metadata = {
            "question_id": q.get("question_id", ""),
            "marks": q.get("marks", ""),
            "question_type": q.get("question_type", ""),
            "topic": q.get("topic", ""),
            "supporting_images": ", ".join(q.get("supporting_images", [])),
        }
        docs.append(Document(page_content=content, metadata=metadata))

    vectordb = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(), persist_directory=persist_directory)
    vectordb.persist()
    print(f"✅ Stored {len(docs)} questions to Chroma at {persist_directory}")

    # 🧪 Test it independently
if __name__ == "__main__":
    store_questions_to_vector_db("outputs/questions_combined.json")

    vectordb = get_vector_store()
    results = vectordb.similarity_search("pythagoras", k=1)

    for r in results:
        print(f"\nQuestion: {r.page_content}")
        print(f"Metadata: {r.metadata}")