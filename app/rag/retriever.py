from langchain.vectorstores import FAISS
from app.rag.embeddings import get_embedding_model
from app.core.config import settings


def get_retriever():
    embedding_model = get_embedding_model()

    vectorstore = FAISS.load_local(
        settings.VECTOR_DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever