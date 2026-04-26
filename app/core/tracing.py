import os
from app.core.config import settings


def setup_tracing():
    os.environ["LANGCHAIN_TRACING_V2"] = settings.LANGCHAIN_TRACING_V2 or "false"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY or ""
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT or "default"
