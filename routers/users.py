from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import (
    UserCreate,
    UserResponse,
    PostResponse
)

router = APIRouter()

@router.get("", response_model=list[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == user.username),
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    new_user = models.User(
        username=user.username,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == username),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.get("/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post).where(models.Post.user_id == user_id)
    )
    posts = result.scalars().all()
    return posts

@router.get("/{user_id}/joins", response_model=list[PostResponse])
def get_user_joins(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post)
        .join(models.Participant)
        .where(models.Participant.user_id == user_id)
    )
    posts = result.scalars().all()
    return posts

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def leave_plan(post_id: int, user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Participant).where(
            models.Participant.post_id == post_id,
            models.Participant.user_id == user_id,
        )
    )
    participant = result.scalars().first()
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participation not found",
        )
    db.delete(participant)
    db.commit()