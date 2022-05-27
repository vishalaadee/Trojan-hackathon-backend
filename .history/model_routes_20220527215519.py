import email,io,xlsxwriter,ast,json
from io import BytesIO
from fastapi import File,UploadFile,Form,Body,Response,FastAPI, BackgroundTasks,APIRouter,status,Depends
# from fastapi.responses import StreamingResponse
from typing import List, Optional
from fastapi.exceptions import HTTPException
from .schemas import User,Doctor,DoctorLoginModel,Appointments,PatientLoginModel,EmailSchema,MessageSchema
from .models import User,Doctor,DoctorLoginModel,Appointments,PatientLoginModel
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi_jwt_auth import AuthJWT
from .database import Base,engine,Session
from fastapi.encoders import jsonable_encoder
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
    )

session=Session(bind=engine)

@auth_router.post("/home/symptoms/{patient_id}")
def enter_symptoms(patient_id:int,symptoms:List[int]):
    df=pd.read_csv(r'C:\Users\HP\Desktop\Trojan-Code\Training.csv')
    df.drop(df.columns[3:127],axis=1,inplace=True)
    train_df = df.drop('Unnamed: 133', axis=1)
    #need to pickle the model
    test_df=pd.read_csv(r'C:\Users\HP\Desktop\Trojan-Code\Testing.csv')
    test_df.drop(test_df.columns[3:127],axis=1,inplace=True)
    x=train_df.iloc[:,:-1]
    y=train_df.iloc[:,8]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
    tree = DecisionTreeClassifier()
    tree.fit(x_train, y_train)
    input_data = symptoms

    input_data_as_numpy_array= np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = tree.predict(input_data_reshaped)

    return prediction[0]

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
        


@auth_router.post("/auth/register",status_code=status.HTTP_201_CREATED)
async def register(name:str,email:EmailStr,password:db: session = Depends(get_db)) -> JSONResponse:
     usn=usn.upper()
     usn=usn.strip()
     email=email.strip()
     db_email=session.query(User).filter(User.email==email).first()
     db_usn=session.query(User).filter(User.usn==usn).first()
     
     if db_usn and (db_usn.email==email) and db_cred==None:
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="your password is "+a,
        
            )
        a=generate_password_hash(a)
        credentials=Credentials(usn=usn,password=a,activated=True)
        session.add(credentials)
        session.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     elif db_usn and (db_usn.email==email) and (db_cred.activated==True):
        return JSONResponse(status_code=200, content={"message": "Account Already Activated"})
     else:
        return JSONResponse(status_code=200, content={"message": "invalid response"})
        
@auth_router.post("/auth/forgot_password",status_code=status.HTTP_201_CREATED)
async def forgot_pass(usn:str,email: EmailStr,db: session = Depends(get_db)) -> JSONResponse:
     usn=usn.upper()
     usn=usn.strip()
     db_email=session.query(User).filter(User.email==email).first()
     db_usn=session.query(User).filter(User.usn==usn).first()
     db_cred=session.query(Credentials).filter(Credentials.usn==usn).first()
     if db_usn and (db_usn.email==email) and db_cred!=None:
        db_user= crud.get_item_by_credentials(db,usn)
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="your password is "+a,
        
            )
        a=generate_password_hash(a)
        db_user[0].password=a
        db.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     elif db_usn and (db_usn.email==email) and (db_cred==None):
        return JSONResponse(status_code=200, content={"message": "Account yet not activated"})
     else:
         return JSONResponse(status_code=200, content={"message": "invalid response"})     

@auth_router.post("/home/password/changepassword/{usn}")
def change_password_student(usn:str,oldpass:str,newpass:str,db:Session=Depends(get_db)):
    usn=usn.upper()
    usn=usn.strip()
    db_user= crud.get_item_by_credentials(db,usn)
    if db_user and check_password_hash(db_user[0].password,oldpass):
        newpass=generate_password_hash(newpass)
        db_user[0].password=newpass
        db.commit()
        return {"message":"Password changed successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong Password")
