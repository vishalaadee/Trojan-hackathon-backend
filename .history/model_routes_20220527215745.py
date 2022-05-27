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
async def register(name:str,email:EmailStr,password:str,phone:str,qualification:str,designation:str,db: session = Depends(get_db)) -> JSONResponse:
