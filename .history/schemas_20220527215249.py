from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.sql.sqltypes import Date, DateTime,Integer
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


class Settings(BaseModel):
    authjwt_secret_key:str='2e5e1aba5ca352882e6a71e553bac6eb71a6b4fae15927e3bee3e0b5394e27b5'

class User(BaseModel):
    p_name:str
    p_email:EmailStr
    p_password:str
    p_phone:str
    p_blood_type:str
    p_dob:datetime
    p_gender:str
    
class Doctor(BaseModel):
    d_name:str
    d_email:EmailStr
    d_password:str
    d_phone:str
    d_qualification:str
    d_designation:str
        
class DoctorLoginModel(BaseModel):
    d_name:str
    password:str
    
class PatientLoginModel(BaseModel):
    d_name:str
    password:str

class Appointments(BaseModel):
    p_id:int
    d_id:int
    status:str
    
class EmailSchema(BaseModel):
   email: List[EmailStr]
   class config:
        orm_mode=True
        arbitrary_types_allowed = True
        

class MessageSchema(BaseModel):
    subject: str
    recipients: List[EmailStr]
    body: str
    sender:str
    class config:
        orm_mode=True
        arbitrary_types_allowed = True

class RegisterDoctor(BaseModel):
    d_name:str
    d_email:EmailStr
    d_password:str
    d_phone:str
    d_qualification:str
    d_designation:str
    class config:
        orm_mode=True
        arbitrary_types_allowed = True
class RegisterPatient(BaseModel):
    p_name:str
    p_email:EmailStr
    p_password:str
    p_phone:str
    p_blood_type:str
    p_dob:datetime
    p_gender:str
    class config:
                