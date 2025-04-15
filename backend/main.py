# Standard library imports
from datetime import datetime, timezone
from typing import Optional, List

# Third-party imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, create_engine, select
import uvicorn

"""
FastAPI backend for Crane Management System
- JWT authentication
- PostgreSQL integration
- Workorder and inventory endpoints (to be implemented)
"""

app = FastAPI(title="Crane Management System Backend")

# Allow CORS from localhost frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8888"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Database setup
DATABASE_URL = "sqlite:///./crane_app.db"
engine = create_engine(DATABASE_URL, echo=False)

# User table for SQLModel (database model)
class UserTable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    disabled: Optional[bool] = False

# Create tables and default admin user
def create_db_and_default_user():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        user = session.exec(select(UserTable).where(UserTable.username == "admin")).first()
        if not user:
            admin = UserTable(username="admin", hashed_password="secret", disabled=False)
            session.add(admin)
            session.commit()

create_db_and_default_user()

# Pydantic schemas for API
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

def fake_hash_password(password: str) -> str:
    """Fake password hashing for demonstration. Replace with real hashing in production."""
    return password

def authenticate_user_db(username: str, password: str):
    """Authenticate user against the SQLite database."""
    with Session(engine) as session:
        user = session.exec(select(UserTable).where(UserTable.username == username)).first()
        if not user or fake_hash_password(password) != user.hashed_password:
            return None
        return user

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token."""
    user = authenticate_user_db(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    # In production, generate JWT here
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}

@app.get("/api/users/me", response_model=User)
def read_users_me(token: str = Depends(oauth2_scheme)):
    # In production, decode JWT and get user
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(username="admin")

# Workorder SQLModel and endpoints

class Workorder(SQLModel, table=True):
    """SQLModel for Workorder table."""
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    location: str = ""
    technician: str = ""
    status: str = "in_progress"  # could be: in_progress, closed, completed
    # Use timezone-aware UTC datetimes for best practice
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Ensure Workorder table is created
SQLModel.metadata.create_all(engine)

@app.get("/api/workorders", response_model=List[Workorder])
def list_workorders(token: str = Depends(oauth2_scheme)):
    """List all workorders."""
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    with Session(engine) as session:
        workorders = session.exec(select(Workorder)).all()
        return workorders

@app.get("/api/workorders/{workorder_id}", response_model=Workorder)
def get_workorder(workorder_id: int, token: str = Depends(oauth2_scheme)):
    """Fetch a single workorder by ID."""
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    with Session(engine) as session:
        workorder = session.get(Workorder, workorder_id)
        if not workorder:
            raise HTTPException(status_code=404, detail="Workorder not found")
        return workorder

@app.post("/api/workorders", response_model=Workorder)
def create_workorder(workorder: Workorder, token: str = Depends(oauth2_scheme)):
    """Create a new workorder."""
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    with Session(engine) as session:
        now = datetime.utcnow()
        db_workorder = Workorder(
            title=workorder.title,
            description=workorder.description,
            location=workorder.location,
            technician=workorder.technician,
            status=workorder.status,
            created_at=now,
            updated_at=now,
        )
        session.add(db_workorder)
        session.commit()
        session.refresh(db_workorder)
        return db_workorder

@app.put("/api/workorders/{workorder_id}", response_model=Workorder)
def update_workorder(workorder_id: int, workorder: Workorder, token: str = Depends(oauth2_scheme)):
    """Update a workorder and set updated_at to now."""
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    with Session(engine) as session:
        db_workorder = session.get(Workorder, workorder_id)
        if not db_workorder:
            raise HTTPException(status_code=404, detail="Workorder not found")
        db_workorder.title = workorder.title
        db_workorder.description = workorder.description
        db_workorder.location = workorder.location
        db_workorder.technician = workorder.technician
        db_workorder.status = workorder.status
        db_workorder.updated_at = datetime.utcnow()
        session.add(db_workorder)
        session.commit()
        session.refresh(db_workorder)
        return db_workorder

@app.delete("/api/workorders/{workorder_id}")
def delete_workorder(workorder_id: int, token: str = Depends(oauth2_scheme)):
    """Delete a workorder by ID."""
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    with Session(engine) as session:
        workorder = session.get(Workorder, workorder_id)
        if not workorder:
            raise HTTPException(status_code=404, detail="Workorder not found")
        session.delete(workorder)
        session.commit()
        return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
