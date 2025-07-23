from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

def create_vector_store_from_text(text, persist_path="chroma_store"):
    """
    Create a vector store from the provided text and persist it.
    Args:
        text (str): The text to embed and store.
        persist_path (str): The directory to persist the vector store.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(text)]

    embeddings = OpenAIEmbeddings()
    
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_path
    )
    db.persist()
    return db

def load_vector_store(persist_path="chroma_store"):
    """
    Load the vector store from the specified directory.
    Args:
        persist_path (str): The directory where the vector store is persisted.
    Returns:
        Chroma: The loaded vector store.
    """
    embeddings = OpenAIEmbeddings()
    db = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_path
    )
    return db

