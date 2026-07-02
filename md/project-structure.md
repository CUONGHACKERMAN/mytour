# Project Architecture & Tech Stack

## Tech Stack
* **Framework**: Python FastAPI
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy (v2.0+)
* **Migrations**: Alembic
* **Validation / Serialization**: Pydantic (v2)

---

## Architectural Overview: Flat Domain-Driven Design (DDD)
This system follows Domain-Driven Design (DDD) principles using a flat, non-nested directory structure. Core infrastructure (database, config, generic base repository) resides in `app/core/`, while business domains are organized cleanly inside `app/domains/`.

---

## Project Directory Structure

```
backend/
├── alembic/                  # Database migrations managed by Alembic
│   ├── versions/
│   └── env.py
├── app/
│   ├── core/                 # Shared core & infrastructure (flat)
│   │   ├── config.py         # App settings & environment variables
│   │   ├── database.py       # SQLAlchemy engine & session dependency
│   │   ├── security.py       # Authentication & RBAC helpers
│   │   ├── tenant.py         # Multi-tenant context & middleware
│   │   └── repository.py     # Generic CRUD Repository (BaseRepository)
│   │
│   └── domains/              # Business domain modules (shallow layout)
│       ├── tour/
│       │   ├── router.py     # FastAPI endpoints for tours
│       │   ├── service.py    # Tour domain business logic
│       │   ├── models.py     # SQLAlchemy ORM models
│       │   └── schemas.py    # Pydantic request/response validation
│       │
│       ├── booking/
│       │   ├── router.py
│       │   ├── service.py
│       │   ├── models.py
│       │   └── schemas.py
│       │
│       ├── resource/         # Accommodation, vehicles, tickets, personnel
│       │   ├── router.py
│       │   ├── service.py
│       │   ├── models.py
│       │   └── schemas.py
│       │
│       └── customer/
│           ├── router.py
│           ├── service.py
│           ├── models.py
│           └── schemas.py
│
├── alembic.ini               # Alembic configuration
├── main.py                   # FastAPI app creation & router registration
└── requirements.txt
```

---

## Shared Generic Repository Pattern (`app/core/repository.py`)
In SQLAlchemy, the `BaseRepository` provides generic CRUD methods while automatically applying tenant isolation.

### Implementation Features:
* **Generic CRUD**: `get()`, `get_multi()`, `create()`, `update()`, `remove()`.
* **Resource Parameterization**: Instantiated with specific SQLAlchemy ORM models (`BaseRepository(TourModel)`).
* **Automatic Tenant Filtering**: Queries automatically append `tenant_id` filters based on the active request's tenant context.
