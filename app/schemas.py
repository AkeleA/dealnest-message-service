from pydantic import BaseModel, Field

class MessageCreate(BaseModel):
    sender_id: int
    recipient_id: int
    body: str = Field(min_length=1)

class MarkReadIn(BaseModel):
    message_id: int

class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    body: str
    is_read: bool

    class Config:
        from_attributes = True
