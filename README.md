# Cher CRM Backend

A RESTful API for a real estate CRM lead management system. Built as a full-stack developer technical assessment for [Cher](https://cheralpha.com), a mortgage fintech company.

The assignment required building a complete lead management system where real estate agents track clients, log interactions, and view analytics. I focused my time on the backend: authentication, data modeling, CRUD operations, and dashboard analytics.

## Tech stack

- **Framework:** FastAPI (Python)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic v2
- **Auth:** JWT tokens (python-jose) with password hashing (passlib)
- **Database:** SQLite (dev), PostgreSQL-ready (psycopg2-binary included)
- **CORS:** FastAPI middleware for frontend communication

## What I built

**Authentication** (JWT-based)
- User registration with duplicate username/email checks
- Login via OAuth2 password flow, returns JWT access token
- Protected `/auth/me` endpoint for session validation
- Token expiration configurable via environment variables

**Lead management** (full CRUD)
- Create, list, view, update, and delete leads
- Soft deletes (sets `is_active = False` instead of removing records)
- Pagination with `skip` and `limit` query parameters
- Duplicate email prevention on lead creation
- Partial updates via PATCH with `model_dump(exclude_unset=True)`

**Activity tracking**
- Log interactions (calls, emails, meetings, notes) against leads
- Filter activities by `lead_id`
- Automatic `activity_count` tracking on the parent lead
- Activity count decrements on deletion

**Dashboard analytics**
- Total leads, total activities
- New leads this week (calculated from current week start)
- Closed leads this month (bounded by month start/end)
- Leads grouped by status
- 10 most recent activities across all leads

## Project structure

```
app/
├── main.py                  # FastAPI app, CORS, lifespan init
├── core/
│   └── database.py          # SQLAlchemy engine, session, init_db
├── models/
│   └── models.py            # User, Lead, Activity table definitions
├── schemas/
│   └── schemas.py           # Pydantic request/response models
├── routers/
│   ├── auth.py              # Register, login, me
│   ├── leads.py             # Lead CRUD
│   ├── activities.py        # Activity CRUD
│   └── dashboard.py         # Analytics endpoint
└── deps/
    └── auth.py              # Password hashing, JWT creation, get_current_user
```

## API endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Create a new user account |
| POST | /auth/login | No | Login, returns JWT token |
| GET | /auth/me | Yes | Get current user profile |
| POST | /leads | Yes | Create a new lead |
| GET | /leads | Yes | List leads (paginated) |
| GET | /leads/{id} | Yes | Get lead details |
| PATCH | /leads/{id} | Yes | Update lead fields |
| DELETE | /leads/{id} | Yes | Soft delete a lead |
| POST | /activities | Yes | Log an activity for a lead |
| GET | /activities | Yes | List activities (filter by lead_id) |
| GET | /activities/{id} | Yes | Get activity details |
| PATCH | /activities/{id} | Yes | Update an activity |
| DELETE | /activities/{id} | Yes | Delete an activity |
| GET | /dashboard | Yes | Get analytics and metrics |

Full interactive API docs available at `/docs` when the server is running.

## Running locally

```bash
git clone https://github.com/Maame-Yaa/Cher-Backend.git
cd Cher-Backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The app creates a SQLite database (`dev.db`) automatically on first run. No manual migration needed.

**Environment variables (optional):**
```
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Frontend companion

The frontend for this project is a minimal React + TypeScript test interface focused on verifying API integration. See [Cher-Frontend](https://github.com/Maame-Yaa/Cher-Frontend).

## Context

This was a 48-hour take-home assignment. I prioritized the backend (authentication, leads, activities, dashboard) and built a functional frontend to verify the API integration. The assignment spec and evaluation criteria focused heavily on API design, database integration, and code quality.
