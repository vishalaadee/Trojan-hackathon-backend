from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import Date, DateTime, Float,Integer
from .database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey

    
class User(Base):
    __tablename__='patients'
    name=Column(String(100),unique=False)
    email=Column(String(80),unique=False)
    password=Column(String(80),unique=False)
    phone=Column(String(14),unique=False)
    secondary_phone=Column(String(14),unique=False,default=Null)
    verified=Column(Integer,default=0)
    def __repr__(self):
        return f"<User {self.name}"
