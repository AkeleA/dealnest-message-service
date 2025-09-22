# DealNest Unread Message Notification Service

A minimal **FastAPI + Celery + Redis** project that implements an event-driven **unread message notification system**.

If a recipient does not read a message within their configured delay window, they receive an email notification (mocked to console logs).If they read the message in time, the pending notification is canceled.

## Features

- **Models**

  - User: id, email, name, notification_delay_minutes
  - Message: sender, recipient, body, is_read, created_at, notification_task_id

- **APIs**

  - POST /messages/: create a message, schedule delayed notification
  - POST /messages/mark-read/: mark as read, cancel pending notification

- **Tasks**

  - Celery worker schedules email notifications with a per-user configurable delay
  - Cancel/revoke jobs when message is read

- **Config**

  - Defaults to SQLite + Redis
  - Mock emailer logs to console

- **Tests**

  - Pytest suite for endpoints and tasks

## Requirements

- Python **3.11+**
- Redis **7+**(run locally with Docker, or use a hosted Redis)
- SQLite (built-in, no setup needed)

## Setup

Clone and install dependencies:

```bash
git clone https://github.com/<your-username>/dealnest-unread-service.git
cd dealnest-unread-service
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Copy the sample file:

```bash
cp .env.example .env
```

.env.example

```bash
# Database connection (SQLite by default)
DATABASE_URL=sqlite:///./app.db

# Redis broker for Celery
REDIS_URL=redis://localhost:6379/0

# Default delay if user.notification_delay_minutes is NULL
DEFAULT_NOTIFICATION_DELAY_MINUTES=1

# Mock email sender (only shown in logs)
EMAIL_SENDER=noreply@dealnest.test

# Celery eager mode (for tests only: set true)
CELERY_TASK_ALWAYS_EAGER=false
```

## Database

Run migrations:

```bash
alembic upgrade head
```

Add some test users:

```bash
sqlite3 app.db \
'insert into users (id,email,name,notification_delay_minutes) values (1,"alice@test.com","Alice",1),(2,"bob@test.com","Bob",2);'
```

## Run the Services

Start Redis

```bash
docker run --name redis -p 6379:6379 -d redis:7
```

Start API

```bash
uvicorn app.main:app --reload
```

Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Start Celery Worker

```bash
celery -A app.tasks.celery_app worker -l info
```

## Usage

Create a message

```bash
curl -X POST http://127.0.0.1:8000/messages/ \
  -H "Content-Type: application/json" \
  -d '{"sender_id":1,"recipient_id":2,"body":"Hello Bob!"}'
```

Worker logs scheduling a notification (countdown = 2 minutes for Bob).

## Mark as read

```bash
curl -X POST http://127.0.0.1:8000/messages/mark-read/ \
  -H "Content-Type: application/json" \
  -d '{"message_id":1}'
```

Worker revokes the scheduled task.

## Let delay expire

After delay, worker logs a mock email:

```bash
MOCK EMAIL -> to=bob@test.com subject='You have unread messages' body='You have 1 unread messages. Visit /messages to read them.' sender=noreply@dealnest.test
```

## Tests

Run the test suite:

```bash
pytest -v
```

## Notes

- Emails are **mocked** to logs. Replace app/emailer.py with SMTP/Mailgun/SendGrid integration for real delivery.
- This is a **minimal demo**. For production: add error handling, retries, monitoring, and a proper transactional outbox for events.
