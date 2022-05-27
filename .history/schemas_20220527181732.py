from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.sql.sqltypes import Date, DateTime,Integer
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


class Settings(BaseModel):
    authjwt_secret_key:str='2e5e1aba5ca352882e6a71e553bac6eb71a6b4fae15927e3bee3e0b5394e27b5'


class LoginModel(BaseModel):
    usn:str
    password:str