from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import schemas, models
from repository import utility
import jwtToken as jwttoken
import hashing

router = APIRouter(
    tags=['Authentication'],
    prefix='/auth'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.ResponseRegister)
def registerUser(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = utility.getUserByEmail(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return utility.createUser(user, db)
    
@router.post("/loginToken", response_model=jwttoken.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = utility.getUserByEmail(db, email=user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found")
    if not hashing.getVerified(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=jwttoken.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwttoken.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

