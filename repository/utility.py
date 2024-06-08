
from fastapi import HTTPException,status
from typing import Optional
from sqlalchemy.orm import Session

from database import SessionLocal
import models, schemas,hashing

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def createUser(User: schemas.CreateUser, db: Session):
    hashedPassword = hashing.getPasswordHashed(User.password)
    User.password = hashedPassword
    user_object = models.User(email=User.email,password=hashedPassword)
    db.add(user_object) 
    db.commit() 
    db.refresh(user_object) 
        
    return user_object

def getUserByEmail(db:Session,email:str):
    return db.query(models.User).filter(models.User.email==email).first()

def checkUser(db:Session ,email:str,password:str):
    user=db.query(models.User).filter(models.User.email==email).first()
    verification=hashing.getVerified(password,user.password)
    return verification


def getUser(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def addToken(db:Session, token:str,typeofToken:str,userId:int):
    newToken=models.Token(tokenstring=token,userId=userId,typeOfToken=typeofToken)

    db.add(newToken)
    db.commit()
    db.refresh(newToken)
    return newToken
# tokenlist=utility.getToken(db,userId==user.id,typeOfToken=tokenReq.typeOfToken)
def getTokens(db:Session, userId:int,typeOfToken:str):
    token=db.query(models.Token).filter(models.Token.userId == userId, models.Token.typeOfToken==typeOfToken).all()
    return token

def deleteToken(db: Session, userId: int,  tokenId: Optional[int] = None):
    output:schemas.Token=None
    if tokenId is None:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either tokenId or typeOfToken must be provided")
    token = db.query(models.Token).filter(models.Token.TokenId == tokenId, models.Token.userId == userId).first()
    if  token:
        output=token
        db.delete(token)
    db.commit()
    return output