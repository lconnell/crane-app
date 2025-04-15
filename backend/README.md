# Crane App Backend

This is the backend for the Crane Shop Management application, built with **FastAPI** and **SQLite**.

## Features
- REST API for workorder and inventory management
- JWT-based authentication
- CORS enabled for frontend communication
- Simple SQLite database (`crane_app.db`)

## Project Structure
- `main.py` – Main FastAPI application
- `crane_app.db` – SQLite database file
- `requirements.txt` – Python dependencies

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Run the backend server
```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## Authentication
- JWT tokens are issued on login and required for protected endpoints.
- Store the token in the frontend (see frontend README).

## Database
- Uses SQLite (`crane_app.db`) by default.
- To reset the DB, delete `crane_app.db` and restart the server (will recreate with empty tables).

## API Endpoints
- `/api/workorders` – CRUD for workorders
- `/api/inventory` – CRUD for inventory parts
- `/api/auth/login` – Obtain JWT token

---
For more details, see the root README or the frontend README.


This directory will contain the FastAPI backend implementation for the Crane Management System.

## Next Steps
- Implement authentication endpoints
- Connect to PostgreSQL database
- Expose RESTful APIs for work order and inventory management

---

**Note:** The frontend codebase has been moved to `/frontend`. Continue all backend development here.
