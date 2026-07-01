from pydantic import BaseModel
from typing import Optional


class RetrieveRequest(BaseModel):
    query: str
    intent: Optional[str] = None
    top_k: int = 10