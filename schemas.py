from datetime import datetime, time
from pydantic import BaseModel, ConfigDict, Field
from enums import OrderType

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PostBase(BaseModel):
    restaurant: str = Field(min_length=1, max_length=100)
    order: OrderType
    departure: datetime
    notes: str | None = None


class PostCreate(PostBase):
    user_id: int
    departure: time


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_posted: datetime
    author: UserResponse