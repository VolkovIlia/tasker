# Tasker

Microservice architecture scaffold for a Telegram bot that turns chat messages into tasks and documents.
All services are accessible through a unified API gateway that performs simple round-robin load balancing.

## Services

- **api-gateway** – single entrypoint and load balancer for all internal services.
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
3. Access the API gateway at `http://localhost:8080`.
4. Internal services run in the Docker network and are not exposed directly.
5. Supporting dependencies:
   - qdrant (vector-db): `http://localhost:6333`
   - minio (object-store): `http://localhost:9000`

This repository currently contains only a minimal skeleton intended for further development. Each service includes basic tests; run them with:

```bash
pytest
```
