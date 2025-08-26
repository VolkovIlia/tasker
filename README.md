# Tasker

Minimal microservice architecture featuring an API gateway and a Telegram bot
service.  The services use a tiny in-repository stub of FastAPI so that the
codebase can be executed and tested without external dependencies.

## Setup and Testing

1. Ensure a recent version of **Python (3.11+)** is available.
2. Clone the repository and optionally create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. The repo vendors small stubs of both **FastAPI** and the
   ``python-telegram-bot`` library, so no extra packages are required for local
   tests.  To verify everything works run:

   ```bash
   pytest
   ```
   All tests should pass.

## Services

- **api-gateway** – single entry point that forwards requests to internal
  services using round-robin load balancing.
- **bot** – Telegram webhook handler supporting `/ping`, `/who` and `/task`
  commands and demonstrating Telegram menu configuration.
- **task** – in-memory task management service exposing `POST /tasks` and
  `GET /tasks` endpoints.

## Development

The repository contains unit tests for both services.  To run them simply
execute:

```bash
pytest
```

## Running with Docker

`docker-compose.yml` describes how the services could be containerised.  Building
these images requires an Internet connection to install the real FastAPI
package.  Launch the stack with:

```bash
docker-compose up --build
```

## `/task` Command

Create a task directly from chat by typing:

```
/task <title> [@assignee] [YYYY-MM-DD] [#tag1 #tag2]
```

Example:

```
/task finish report @alice 2024-12-31 #work #urgent
```

The bot forwards the request to the API gateway which creates the task in the
task service and replies with the new task identifier.
