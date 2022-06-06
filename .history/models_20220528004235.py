from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import Date, DateTime, Float,Integer
from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey

    
class User(Base):
    __tablename__='patients'
    p_id=Column(Integer,primary_key=True)
    p_name=Column(String(100),unique=False)
    p_email=Column(String(80),unique=False)
    p_age=Column(Integer,unique=False)
    p_gender=Column(String(1),unique=False)
    p_phone=Column(String(14),unique=False)
    p_blood_type=Column(String(14),unique=False)
    def __repr__(self):
        return f"<User {self.name}"

class Doctor(Base):
    __tablename__='doctors'
    d_id=Column(Integer,primary_key=True)
    d_name=Column(String(100),unique=False)
    d_email=Column(String(80),unique=False)
    d_phone=Column(String(14),unique=False)
    d_qualification=Column(String(104),unique=False)
    d_description=Column(String(104),unique=False)
    d_expertise=Column(String(100),unique=False)
    def __repr__(self):
        return f"<Doctor {self.name}"

class Credentials(Base):
    __tablename__ ='credentials'
    email=Column(String(12),primary_key=True,unique=True)
    password=Column(String(50),unique=False)
    activated=Column(Boolean,default=False)
    def __repr__(self):
        return f"<Cred {self.name}"

class Appointments(Base):
    __tablename__='appointments'
    a_id=Column(Integer,primary_key=True)
    d_id=Column(Integer,ForeignKey('doctors.d_id'))
    p_id=Column(Integer,ForeignKey('patients.p_id'))
    status=Column(String(1),unique=False,default)
    def __repr__(self):
        return f"<Appointment {self.name}"
