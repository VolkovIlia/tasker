# Tasker

Microservice architecture scaffold for a Telegram bot that turns chat messages into tasks and documents.

## Services

- **bot** – Telegram webhook handler and command router.
- **task-service** – CRUD for tasks and reminders.
- **doc-service** – Generates meeting protocols, checklists, and sprint plans.
- **reminder-service** – Schedules and fires reminders.
- **db** – PostgreSQL storage for metadata.
- **vector-db** – Qdrant instance for RAG-light.
- **object-store** – S3-compatible bucket for attachments.

## Getting Started

1. Install [Docker](https://docs.docker.com/get-docker/).
2. Start the stack:
   ```bash
   docker-compose up --build
   ```
3. Services will be available on the following ports:
   - bot: `http://localhost:8000`
   - task-service: `http://localhost:8001`
   - doc-service: `http://localhost:8002`
   - reminder-service: `http://localhost:8003`
   - qdrant (vector-db): `http://localhost:6333`
   - minio (object-store): `http://localhost:9000`

This repository currently contains only a minimal skeleton intended for further development.
