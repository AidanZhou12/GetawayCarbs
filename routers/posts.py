from typing import Annotated
from datetime import datetime, time
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import (
    PostCreate,
    PostResponse
)
from sqlalchemy.orm import selectinload

router = APIRouter()

@router.get("", response_model=list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).options(selectinload(models.Post.author)))
    posts = result.scalars().all()
    return posts

@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    departure = datetime.combine(datetime.now().date(), post.departure)
    new_post = models.Post(
        restaurant=post.restaurant,
        order=post.order,
        departure=departure,
        notes=post.notes,
        author=user,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post