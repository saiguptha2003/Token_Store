from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Literal,Optional

class CreateUser(BaseModel):
    email:str 
    password:str 
    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    email:str
    password:str
    class Config:
        orm_mode = True

class ResponseRegister(BaseModel):
    email:str
    class Config:
        orm_mode = True
class ResponseLogin(BaseModel):
    email:str
    class Config:
        orm_mode = True


class AddToken(BaseModel):
    token:str
    typeofToken:str
    class Config:
        orm_mode = True 

class ResponseAddToken(BaseModel):
    createdTime:datetime  
    status:str
    email:str
    class Config:
        orm_mode = True  
    

class ResponseTokenObject(BaseModel):
    TokenId: int
    email: str
    tokenstring: str
    typeOfToken: str
    createTime: datetime
    class Config:
        orm_mode=True
        
class RequestToken(BaseModel):
    typeOfToken:str
    class Config:
        orm_mode=True
class Token(BaseModel):
    TokenId: int
    tokenstring: str
    typeOfToken: str
    createTime: datetime
    
    
class ReqDeleteToken(BaseModel):
    TokenId: Optional[int]
    
class ResponseDeleteToken(BaseModel):
    TokenId: int
    tokenstring: str
    typeOfToken:str
    createTime:datetime
    