from celery import Celery
from celery.result import AsyncResult
from sqlalchemy.orm import Session
from typing import Iterator
from contextlib import contextmanager
from . import config
from .database import SessionLocal
from . import models, crud
from .emailer import send_email

settings = config.settings

celery_app = Celery(
    "dealnest",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
)

@contextmanager
def db_sess() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@celery_app.task(name="send_unread_notification")
def send_unread_notification(message_id: int):
    with db_sess() as db:
        msg = db.get(models.Message, message_id)
        if not msg or msg.is_read:
            return
        count = crud.unread_count_for_user(db, msg.recipient_id)
        subject = "You have unread messages"
        body = f"You have {count} unread messages. Visit /messages to read them."
        send_email(to_email=msg.recipient.email, subject=subject, body=body)

@celery_app.task(name="handle_event")
def handle_event(event_type: str, payload: dict):
    with db_sess() as db:
        if event_type == "MessageCreated":
            message_id = int(payload["message_id"])
            msg = db.get(models.Message, message_id)
            if not msg:
                return
            delay_min = crud.get_user_notification_delay(
                db, msg.recipient_id, settings.DEFAULT_NOTIFICATION_DELAY_MINUTES
            )
            async_res = celery_app.send_task(
                "send_unread_notification",
                args=[message_id],
                countdown=delay_min * 60,
            )
            crud.set_message_task_id(db, message_id, async_res.id)

        elif event_type == "MessageRead":
            message_id = int(payload["message_id"])
            msg = db.get(models.Message, message_id)
            if not msg:
                return
            if msg.notification_task_id:
                AsyncResult(msg.notification_task_id, app=celery_app).revoke()
                crud.clear_message_task_id(db, message_id)

def emit_event(event_type: str, payload: dict) -> None:
    celery_app.send_task("handle_event", args=[event_type, payload])
