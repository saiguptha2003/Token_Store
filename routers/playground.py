
from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import schemas, models
from repository import utility
import jwtToken as jwttoken
import hashing


router=APIRouter(
    tags=['tokenplayground'],
    prefix='/tokenplayground'
    
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await jwttoken.getCurrentUser(token, db)
@router.post("/addToken",response_model=schemas.ResponseAddToken)
async def addToken(tokenObj:schemas.AddToken,user: Annotated[models.User, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    if tokenObj.token==None or tokenObj.typeofToken==None:
        raise HTTPException(status_code=204  ,detail="token and type of token empty")
    if db.query(models.Token).filter(models.Token.tokenstring==tokenObj.token, models.Token.typeOfToken==tokenObj.typeofToken).first():
        raise HTTPException(status_code=404, detail="token details all ready exists")
    tokenresponse=utility.addToken(db,userId=user.id,token=tokenObj.token,typeofToken=tokenObj.typeofToken)
    return schemas.ResponseAddToken(email=user.email,status="success",createdTime=tokenresponse.createTime)
    
    
@router.post("/getToken",response_model=List[schemas.Token])
async def getToken(tokenReq:schemas.RequestToken,user:Annotated[models.User,Depends(get_current_active_user)],db:Session=Depends(get_db)):
    if tokenReq.typeOfToken==None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="pass TypeofToken")
    if db.query(models.Token).filter(models.Token.typeOfToken==tokenReq.typeOfToken).all()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="provide valid Type of Token")
    print(user.email)
    tokenlist=utility.getTokens(db,userId=user.id,typeOfToken=tokenReq.typeOfToken)

    return tokenlist

@router.get("/getAllTokens",response_model=List[schemas.Token] )
def getAllTokens(user:Annotated[models.User,Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return db.query(models.Token).all()

@router.delete("/deleteToken",response_model=schemas.ResponseDeleteToken)
async def deleteToken(delToken:schemas.ReqDeleteToken,user:Annotated[models.User,Depends(get_current_active_user)],db:Session=Depends(get_db)):
    if delToken is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="provide valid details")
    token=utility.deleteToken(db,userId=user.id, tokenId=delToken.TokenId)
    timeOfDelete=datetime.now()

    if token:
        tokensResponse=schemas.ResponseDeleteToken(
            TokenId=token.TokenId,
            tokenstring=token.tokenstring,
            typeOfToken=token.typeOfToken,
            createTime=token.createTime,
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="provide token not found")
    
        
    return tokensResponse
    
    

        
    
    
    