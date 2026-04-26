from fastapi import APIRouter
from app.api.schemas import ChatRequest, ChatResponse
from app.graph.main_graph import build_graph
from fastapi.responses import StreamingResponse
import time

router = APIRouter()

graph = build_graph()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    result = graph.invoke({
        "query": request.query,
        "send_email": request.send_email,
        "user_email": request.user_email
    })

    # Extract source text (simplified)
    sources = []
    for doc in result.get("sources", []):
        sources.append(doc.page_content[:200])  # preview

    return ChatResponse(
        answer=result.get("answer"),
        email_status=result.get("email_status"),
        sources=sources
    )
    
@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    result = graph.invoke({
        "query": request.query,
        "send_email": request.send_email,
        "user_email": request.user_email
    })

    answer = result.get("answer", "")

    def generate():
        for word in answer.split():
            yield word + " "
            time.sleep(0.03)

    return StreamingResponse(generate(), media_type="text/plain")
