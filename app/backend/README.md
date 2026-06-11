# Backend

FastAPI backend for **Stockmaster**.

## Stack

- Python 3.11+
- FastAPI 0.136
- SQLAlchemy 2.0
- PostgreSQL 14+
- Uvicorn

## Source code

The Python application package lives in `app/backend/`.  
Run from the **project root**:

```bash
uvicorn app.backend.main:app --reload
```

## Dependencies

Install from project root (or from this folder):

```bash
pip install -r app/backend/requirements.txt
```

## Database

SQL schema and seed data: `database/create_database.sql`
