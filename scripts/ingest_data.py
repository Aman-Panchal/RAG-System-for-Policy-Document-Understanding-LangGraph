import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from app.rag.embeddings import get_embedding_model
from app.core.config import settings


DATA_PATH = "data/raw"


def load_documents():
    docs = []

    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)

        if file.endswith(".txt"):
            loader = TextLoader(path)
        elif file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            continue

        docs.extend(loader.load())

    return docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


def main():
    print("Loading documents...")
    docs = load_documents()

    print(f"Loaded {len(docs)} documents")

    print("Splitting documents...")
    chunks = split_documents(docs)

    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings...")
    embedding_model = get_embedding_model()

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    print(f"Saving vectorstore to {settings.VECTOR_DB_PATH}")
    vectorstore.save_local(settings.VECTOR_DB_PATH)

    print("Ingestion complete!")


if __name__ == "__main__":
    main()