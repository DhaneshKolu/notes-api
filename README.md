# Notes API

A backend Notes application built with FastAPI and PostgreSQL, featuring JWT authentication and secure CRUD operations.

## Features
- User registration & login
- JWT authentication (OAuth2 Password Flow)
- Notes CRUD with ownership enforcement
- Soft delete (archive & restore)
- PostgreSQL + SQLAlchemy ORM

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (python-jose)
- Passlib (Argon2)

## Setup
```bash
git clone https://github.com/DhaneshKolu/notes-api
cd notes-api
pip install -r requirements.txt
uvicorn app.main:app --reload
