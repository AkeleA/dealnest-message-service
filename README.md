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

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  git clone https://github.com//dealnest-unread-service.git  cd dealnest-unread-service  python -m venv .venv  source .venv/bin/activate   # Windows: .venv\Scripts\activate  pip install -r requirements.txt  `

## Environment Variables

Copy the sample file:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  cp .env.example .env  `

### .env.example

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  # Database connection (SQLite by default)  DATABASE_URL=sqlite:///./app.db  # Redis broker for Celery  REDIS_URL=redis://localhost:6379/0  # Default delay if user.notification_delay_minutes is NULL  DEFAULT_NOTIFICATION_DELAY_MINUTES=1  # Mock email sender (only shown in logs)  EMAIL_SENDER=noreply@dealnest.test  # Celery eager mode (for tests only: set true)  CELERY_TASK_ALWAYS_EAGER=false  `

## Database

Run migrations:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  alembic upgrade head  `

Add test users:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  sqlite3 app.db \  'insert into users (id,email,name,notification_delay_minutes) values (1,"alice@test.com","Alice",1),(2,"bob@test.com","Bob",2);'  `

## Run the services

### Start Redis

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  docker run --name redis -p 6379:6379 -d redis:7  `

### Start API

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  uvicorn app.main:app --reload  `

Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Start Celery worker

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  celery -A app.tasks.celery_app worker -l info  `

## Usage

### Create a message

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  curl -X POST http://127.0.0.1:8000/messages/ \    -H "Content-Type: application/json" \    -d '{"sender_id":1,"recipient_id":2,"body":"Hello Bob!"}'  `

- Worker logs scheduling a notification (countdown = 2 minutes for Bob).

### Mark as read

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  curl -X POST http://127.0.0.1:8000/messages/mark-read/ \    -H "Content-Type: application/json" \    -d '{"message_id":1}'  `

- Worker revokes the scheduled task.

### Let delay expire

- MOCK EMAIL -> to=bob@test.com subject='You have unread messages' body='You have 1 unread messages. Visit /messages to read them.' sender=noreply@dealnest.test

## Tests

Run the test suite:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  pytest -v  `

## Notes

- Emails are **mocked** to logs. Replace app/emailer.py with SMTP/Mailgun/SendGrid integration for real delivery.
- This is a **minimal demo**. For production: add error handling, retries, monitoring, and a proper transactional outbox for events.
