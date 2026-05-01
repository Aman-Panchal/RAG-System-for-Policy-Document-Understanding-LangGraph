from fastapi import FastAPI
from app.api.routes import router
from app.core.tracing import setup_tracing

setup_tracing()

app = FastAPI(title="RAG Policy System")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "RAG Policy System is running"}
