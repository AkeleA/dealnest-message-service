from sqlalchemy.orm import Session
from sqlalchemy import select, func
from . import models

def create_message(db: Session, sender_id: int, recipient_id: int, body: str) -> models.Message:
    msg = models.Message(sender_id=sender_id, recipient_id=recipient_id, body=body)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def mark_message_read(db: Session, message_id: int) -> models.Message | None:
    msg = db.get(models.Message, message_id)
    if not msg:
        return None
    msg.is_read = True
    db.commit()
    db.refresh(msg)
    return msg

def set_message_task_id(db: Session, message_id: int, task_id: str) -> None:
    msg = db.get(models.Message, message_id)
    if msg:
        msg.notification_task_id = task_id
        db.commit()

def clear_message_task_id(db: Session, message_id: int) -> None:
    msg = db.get(models.Message, message_id)
    if msg:
        msg.notification_task_id = None
        db.commit()

def get_user_notification_delay(db: Session, user_id: int, default: int) -> int:
    user = db.get(models.User, user_id)
    if not user or user.notification_delay_minutes is None:
        return default
    return user.notification_delay_minutes

def is_message_read(db: Session, message_id: int) -> bool:
    msg = db.get(models.Message, message_id)
    return bool(msg and msg.is_read)

def unread_count_for_user(db: Session, user_id: int) -> int:
    q = select(func.count(models.Message.id)).where(
        models.Message.recipient_id == user_id,
        models.Message.is_read == False  # noqa: E712
    )
    return int(db.execute(q).scalar_one())
