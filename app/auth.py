from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import models, schemas, crud
from .core.config import settings
from .dependencias import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)

    if not user:
        return False
    
    if not verify_password_hash(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expres_delta: timedelta = None):
    to_encode = data.copy()

    if expres_delta:
        expire = datetime.utcnow() + expres_delta
        
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email)
    
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user