from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import schemas, crud, models
from .tasks import emit_event

app = FastAPI(title="DealNest Unread Message Notification Service")

Base.metadata.create_all(bind=engine)

@app.post("/messages/", response_model=schemas.MessageOut)
def create_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    if not db.get(models.User, payload.sender_id) or not db.get(models.User, payload.recipient_id):
        raise HTTPException(status_code=400, detail="Invalid sender_id or recipient_id")
    msg = crud.create_message(db, payload.sender_id, payload.recipient_id, payload.body)
    emit_event("MessageCreated", {"message_id": msg.id})
    return msg

@app.post("/messages/mark-read/")
def mark_read(input: schemas.MarkReadIn, db: Session = Depends(get_db)):
    msg = crud.mark_message_read(db, input.message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    emit_event("MessageRead", {"message_id": msg.id})
    return {"status": "ok"}
