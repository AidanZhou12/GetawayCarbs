from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from database import Base, engine, get_db
from schemas import (
    PostCreate,
    PostResponse,
    UserCreate,
    UserResponse,
)
from routers import posts, users

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])