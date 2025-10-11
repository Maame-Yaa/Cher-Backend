This repo contains code for a FastAPI backend, with JWT auth, Leads, Activities, and Dashboard

## Stack
- FastAPI, Pydantic
- SQLAlchemy ORM
- SQLite (dev) / PostgreSQL (prod)
- JWT (python-jose)
- Password hashing (passlib/bcrypt)
- CORS for frontend

## Endpoints
- Auth: `/auth/register`, `/auth/login` (OAuth2 password), `/auth/me`
- Leads: `POST /leads`, `GET /leads`, `GET /leads/{id}`, `PATCH /leads/{id}`, `DELETE /leads/{id}`
- Activities: `POST /activities`, `GET /activities?lead_id=...`, etc.
- Dashboard: `GET /dashboard`
- Docs: `/docs`

## Local setup
```bash
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reloadS
