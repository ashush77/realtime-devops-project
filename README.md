# Real-Time DevOps Project

An end-to-end learning project demonstrating application development,
containerization, database persistence, automated testing, CI/CD,
deployment, and monitoring.

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Git and GitHub
- GitHub Actions (planned)
- Terraform (planned)
- Prometheus and Grafana (planned)

## Current Features

- API homepage: GET /
- Application and database health check: GET /health
- Create an item: POST /items
- List items: GET /items
- Dockerized backend
- PostgreSQL database
- Persistent database volume
- Multi-service orchestration with Docker Compose

## Prerequisites

- Docker Desktop
- Git

Python is required for local development outside Docker.

## Run the Application

From the project root, run:

```powershell
docker compose up -d --build