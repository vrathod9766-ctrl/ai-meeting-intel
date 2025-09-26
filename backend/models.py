from pydantic import BaseModel
from typing import Optional

class MeetingCreate(BaseModel):
    filename: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    topics: Optional[str] = None

class MeetingResponse(MeetingCreate):
    id: int

    class Config:
        from_attributes = True
