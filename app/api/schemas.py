from pydantic import BaseModel
from typing import Optional
from typing import List


class ChatRequest(BaseModel):
    query: str
    user_email: Optional[str] = None
    send_email: Optional[bool] = False



class ChatResponse(BaseModel):
    answer: str
    email_status: Optional[str] = None
    sources: Optional[List[str]] = None
