from langchain.embeddings import OpenAIEmbeddings
from app.core.config import settings


def get_embedding_model():
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY
    )