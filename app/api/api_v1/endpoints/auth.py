from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.dependencias import get_db
from app.auth import get_current_active_user


router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

