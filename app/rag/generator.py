from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings


def get_llm():
    return ChatOpenAI(
        model=settings.MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=0.2
    )


def get_prompt():
    template = """
You are an expert assistant for policy document analysis.

Use ONLY the provided context to answer the question.
If the answer is not in the context, say "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer clearly and concisely:
"""

    return ChatPromptTemplate.from_template(template)
