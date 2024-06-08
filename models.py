from datetime import datetime
from sqlalchemy import Boolean , String, Integer, Column,ForeignKey,DateTime

from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True,index=True)
    email=Column(String,unique=True, nullable=False, index=True)
    password=Column(String,nullable=False)
    tokens=relationship("Token",back_populates="owner")
    

class Token(Base):
    __tablename__ = "tokens"
    TokenId = Column(Integer, primary_key=True, index=True)
    typeOfToken = Column(String, nullable=False)
    tokenstring = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey("users.id"))  
    createTime=Column(DateTime, nullable=False, default=datetime.now())
    owner = relationship("User", back_populates="tokens") 
