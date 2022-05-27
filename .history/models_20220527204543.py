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
    phone=Column(String(14),unique=False)
    blood_type=Column(String(14),unique=False)
    def __repr__(self):
        return f"<User {self.name}"

class Doctor(Base):
    __tablename__='doctors'
    name=Column(String(100),unique=False)
    email=Column(String(80),unique=False)
    password=Column(String(80),unique=False)
    dob=Column(DateTime,unique=False)
    gender=Column(String(1),unique=False)
    phone=Column(String(14),unique=False)
    qualification=Column(String(54),unique=False)
    description=Column(String(54),unique=False)
    
    def __repr__(self):
        return f"<Doctor {self.name}"

class Appointment(Base):
    __tablename__='appointments'
    a_id=Column(Integer,primary_key=True)
    d_id=Column(Integer,ForeignKey('doctors.d_id'))
    p_id=
    def __repr__(self):
        return f"<Doctor {self.name}"
