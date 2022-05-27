from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import Date, DateTime, Float,Integer
from .database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey

    
class User(Base):
    __tablename__='patients'
    name=Column(String(100),unique=False)
    email=Column(String(80),unique=False)
    email=Column(String(80),unique=False)
    middle_name=Column(String(25),unique=False)
    last_name=Column(String(25),unique=False)
    branch=Column(String(25),unique=False)
    backlogs=Column(Integer,unique=False)
    ssc=Column(Float,unique=False)
    hsc=Column(Float,unique=False)
    ug=Column(Float,unique=False)
    pg=Column(Float,unique=False)
    ug_percentage=Column(Float,unique=False)
    sem1=Column(Float,unique=False)
    sem2=Column(Float,unique=False)
    sem3=Column(Float,unique=False)
    sem4=Column(Float,unique=False)
    sem5=Column(Float,unique=False)
    sem6=Column(Float,unique=False)
    sem7=Column(Float,unique=False)
    sem8=Column(Float,unique=False)
    current_backlogs=Column(String(30),unique=False)
    history_backlogs=Column(String(30),unique=False)
    no_of_x_grades=Column(Integer,unique=False)
    other_grades=Column(String(30),unique=False)
    ug_start_year=Column(Integer,unique=False)
    ug_end_year=Column(Integer,unique=False)
    ssc_board=Column(String(50),unique=False)
    hsc_board=Column(String(50),unique=False)
    hsc_start_year=Column(Integer,unique=False)
    hsc_end_year=Column(Integer,unique=False)
    ssc_start_year=Column(Integer,unique=False)
    ssc_end_year=Column(Integer,unique=False)
    entry_to_college=Column(String(40),unique=False)
    rank=Column(Integer,unique=False)
    gap_in_studies=Column(String(255),unique=False)
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
