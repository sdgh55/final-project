from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

api = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str


@api.post('/users/')
def create_user(user_data: UserCreate, db: Session = db.session):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
