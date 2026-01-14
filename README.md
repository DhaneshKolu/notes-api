# Notes API

This project is a backend REST API built using FastAPI that allows users to manage personal notes securely.  
Beyond basic CRUD functionality, the project focuses on applying real backend engineering concepts such as observability, caching, background processing, and system health monitoring.

The goal of this project was not just to “build an API”, but to understand how backend systems are designed, optimized, and operated in real-world scenarios.

---

## Tech Stack

- **FastAPI** – API framework
- **PostgreSQL** – primary data store
- **SQLAlchemy** – ORM for database interaction
- **Redis** – in-memory cache
- **JWT Authentication** – secure user authentication
- **Pydantic** – request/response validation and serialization

---

## What the API Does

- Authenticated users can create, read, update, delete, and restore notes
- Notes are user-specific and fully isolated per account
- Deletion is implemented as a soft delete (archiving), allowing safe restoration
- List endpoints are paginated to protect the database and API performance

---

## Backend Engineering Highlights

### Logging & Request Observability
The application uses Python’s logging module to provide consistent and meaningful logs across the system.  
A custom middleware captures request method, path, status code, and execution time, making it easy to identify slow endpoints and trace request behavior during development.

This replaces ad-hoc `print` debugging with structured observability.

---

### Caching with Redis
Redis is used as an in-memory cache for read-heavy endpoints.

- The **cache-aside pattern** is implemented for the `GET /notes` endpoint
- Cache keys are user-scoped and pagination-aware
- Cached data has a short TTL to avoid stale reads
- Cache is explicitly invalidated on create, update, delete, and restore operations

Redis is treated strictly as a performance optimization layer — PostgreSQL remains the single source of truth.

---

### Background Tasks
FastAPI BackgroundTasks are used for non-critical work that does not need to block the request lifecycle.

For example:
- Note deletion triggers background logging/audit work after the response is sent

This keeps API responses fast while still supporting asynchronous backend behavior.

---

### Pagination & Query Protection
All collection-based endpoints are protected with pagination.

- Sensible default limits are enforced
- Maximum limits prevent accidental or malicious heavy queries
- Ownership filtering is applied before pagination to ensure data safety

This ensures the API remains scalable as data grows.

---

### Health & Monitoring
A lightweight `/health` endpoint is implemented to expose service health.

- Verifies database connectivity
- Verifies Redis availability
- Designed to respond quickly without heavy queries

This endpoint is suitable for readiness/liveness checks and basic monitoring setups.

---

## API Endpoints (High-Level)

### Authentication
- `POST /login`

### Notes
- `GET /notes`
- `POST /notes`
- `PUT /notes/{id}`
- `DELETE /notes/{id}`
- `POST /notes/restore/{id}`

### Monitoring
- `GET /health`

---

## Running the Project Locally

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Configure environment variables
5. Start the server

```bash
uvicorn app.main:app --reload
