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
    dob=Column(DateTime,unique=False)
    gender=Column(String(1),unique=False)
    category=Column(String(10),unique=False)
    native=Column(String(10),unique=False)
    parents_name=Column(String(50),unique=False)
    present_addr=Column(Text,unique=False)
    permanent_addr=Column(Text,unique=False)
    phone=Column(String(14),unique=False)
    secondary_phone=Column(String(14),unique=False,default=Null)
    verified=Column(Integer,default=0)
    def __repr__(self):
        return f"<User {self.name}"
