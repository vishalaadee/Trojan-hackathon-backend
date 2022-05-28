from datetime import datetime
import email,io,xlsxwriter,ast,json
from io import BytesIO
from fastapi import File,UploadFile,Form,Body,Response,FastAPI, BackgroundTasks,APIRouter,status,Depends
# from fastapi.responses import StreamingResponse
from typing import List, Optional
from fastapi.exceptions import HTTPException
from schemas import Credentials,User,Doctor,DoctorLoginModel,Appointments,PatientLoginModel,EmailSchema,MessageSchema
from models import User,Doctor,Credentials,Appointments
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi_jwt_auth import AuthJWT
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from database import Base,engine,Session
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

def generate_password():
    import random
    import array

    MAX_LEN = 6

    
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    SYMBOLS = ['@','(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
        password = password + x
    return password


conf = ConnectionConfig(
    MAIL_USERNAME = "placementsjce2022@gmail.com",
    MAIL_PASSWORD = "pradeepsirbcvs123",
    MAIL_FROM = "placementsjce2022@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Placement-Information",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@auth_router.post("/home/symptoms/")
def enter_symptoms(s1:str,s2:str,s3:str,s4:str):
    df=pd.read_csv('Training.csv')
    train_df = df.drop('Unnamed: 133', axis=1)
    #need to pickle the model
    test_df=pd.read_csv('Testing.csv')
    x=train_df.iloc[:,:-1]
    y=train_df.iloc[:,132]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
    tree = DecisionTreeClassifier()
    tree.fit(x_train, y_train)
    input_data=(0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    
    import numpy as np
    # change the input data to a numpy array
    input_data_as_numpy_array= np.asarray(input_data)

    # reshape the numpy array as we are predicting for only on instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = tree.predict(input_data_reshaped)

    # # input_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # input_data=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    # #return len(input_data)
    # # # input_data[0]=1
    # input_data_as_numpy_array= np.asarray(input_data)
    # # # return input_data_as_numpy_array
    
    # input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    
    # prediction = tree.predict(input_data_reshaped)
    # accuracy=accuracy_score(y_test,prediction)
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
        
@auth_router.post("/auth/register_doctor",status_code=status.HTTP_201_CREATED)
async def register_doctor(name:str,email:EmailStr,phone:str,qualification:str,description:str,expertise:str,db: session = Depends(get_db)) -> JSONResponse:
     email=email.upper()
     db_cred=session.query(Credentials).filter(Credentials.email==email).first()
     
     if db_cred==None:
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="hello doctor "+name+" your password is "+a,
        
            )
        #a=generate_password_hash(a)
        a=a.strip()
        credentials=Credentials(email=email,password=a,activated=True)
        details=Doctor(d_name=name,d_email=email,d_phone=phone,d_qualification=qualification,d_description=description,d_expertise=expertise)
        session.add(credentials)
        session.add(details)
        session.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     elif (db_cred!=None) and (db_cred.activated==True):
        return JSONResponse(status_code=200, content={"message": "Account Already Activated"})
     else:
        return JSONResponse(status_code=200, content={"message": "invalid response"})


@auth_router.post("/auth/register_patient",status_code=status.HTTP_201_CREATED)
async def register_patient(name:str,email:EmailStr,phone:str,blood_type:str,age:int,gender:str,db: session = Depends(get_db)) -> JSONResponse:
     email=email.upper()
     db_cred=session.query(Credentials).filter(Credentials.email==email).first()
     
     if db_cred==None:
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="hello"+name+ "your patient password is "+a,
        
            )
        a=a.strip()
        #a=generate_password_hash(a)
        credentials=Credentials(email=email,password=a,activated=True)
        details=User(p_name=name,p_email=email,p_phone=phone,p_blood_type=blood_type,p_age=age,p_gender=gender)
        session.add(details)
        session.add(credentials)
        session.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     elif (db_cred!=None) and (db_cred.activated==True):
        return JSONResponse(status_code=200, content={"message": "Account Already Activated"})
     else:
        return JSONResponse(status_code=200, content={"message": "invalid response"})

@auth_router.post('/doctor_login',status_code=200)
async def doctor_login(email:EmailStr,password:str,Authorize:AuthJWT=Depends()):
    email=email.upper()
    db_user=session.query(Credentials).filter(email==Credentials.email).first()
    password=password.strip()        
    db_password=db_user.password.strip()
    if db_user and (db_password == password) :
        access_token=Authorize.create_access_token(subject=db_user.email)
        refresh_token=Authorize.create_refresh_token(subject=db_user.email)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )


@auth_router.post('/patient_login',status_code=200)
async def patient_login(email:EmailStr,password:str,Authorize:AuthJWT=Depends()):
    email=email.upper()
    db_user=session.query(Credentials).filter(email==Credentials.email).first()
    password=password.strip()
    db_password=db_user.password.strip()
    if db_user and (db_password == password):
        access_token=Authorize.create_access_token(subject=db_user.email)
        refresh_token=Authorize.create_refresh_token(subject=db_user.email)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )


#refreshing tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token"
        ) 

    current_user=Authorize.get_jwt_subject()

    
    access_token=Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access":access_token})


@auth_router.post("/forgot_password",status_code=status.HTTP_201_CREATED)
async def forgot_pass(email: EmailStr,db: session = Depends(get_db)) -> JSONResponse:
     email=email.upper()
     db_cred=session.query(Credentials).filter(Credentials.email==email).first()
     if db_cred!=None:
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="your password is "+a,
        
            )
        a=generate_password_hash(a)
        db_cred[0].password=a
        db.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     elif (db_cred==None):
        return JSONResponse(status_code=200, content={"message": "Account yet not activated"})
     else:
         return JSONResponse(status_code=200, content={"message": "invalid email"})     

@auth_router.post("/home/password/changepassword/{usn}")
def change_password_student(email:EmailStr,oldpass:str,newpass:str,db:Session=Depends(get_db)):
    email=email.upper()
    db_cred=session.query(Credentials).filter(Credentials.email==email).first()
    if db_cred and check_password_hash(db_cred[0].password,oldpass):
        newpass=generate_password_hash(newpass)
        db_cred[0].password=newpass
        db.commit()
        return {"message":"Password changed successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong Credentials")
        
@auth_router.get("/doctor's list")
def doctor_list(db:Session=Depends(get_db)):
    doctors=session.query(Doctor).all()
    return doctors

@auth_router.post("/book appointment/{p_id}/{d_id}")
def book_appointment(pid:int,did:int,db:Session=Depends(get_db)):
    patient=session.query(User).filter(User.p_id==pid).first()
    doctor=session.query(Doctor).filter(Doctor.d_id==did).first()
    status=session.query(Appointments.status).filter(Appointments.p_id==pid).filter(Appointments.d_id==did).all()
    if status!=2:
        return {"message":"Appointment already booked"}
    if patient and doctor:
        appointment=Appointments(p_id=pid,d_id=did,status=0)
        session.add(appointment)
        session.commit()
        return {"message":"Appointment requested successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error in booking appointment")


@auth_router.get("/patient appointments/{p_id}")
def patient_appointments(pid:int,db:Session=Depends(get_db)):
    d_id=session.query(Appointments.d_id).filter(Appointments.p_id==pid).all()
    appointment_details={"doctor_details":[],"status":[]}
    doc_details=db.query(Doctor).filter(Doctor.d_id==d_id).all()
    status=session.query(Appointments.status).filter(Appointments.p_id==pid).all()
    appointment_count=len(d_id)
    for i in range(appointment_count):
        appointment_details["doctor_details"].append(doc_details[i])
        appointment_details["status"].append(status[i])    
    return appointment_details

@auth_router.post("/cancel appointment/{p_id}/{d_id}")
def cancel_appointment(pid:int,did:int,db:Session=Depends(get_db)):
    appointment=session.query(Appointments).filter(Appointments.p_id==pid).filter(Appointments.d_id==did).first()
    if appointment:
        appointment.status=2
        session.commit()
        return {"message":"Appointment cancelled successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error in cancelling appointment")

@auth_router.post("/payment success/{d_id}/{p_id}")
def payment_status(d_id:int,p_id:int,db:Session=Depends(get_db)):
    appointment=session.query(Appointments).filter(Appointments.p_id==p_id).filter(Appointments.d_id==d_id).first()
    if appointment:
        appointment.status=1
        session.commit()
        return {"message":"Payment success"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Appointment Not Done")
@auth_router.get("/doctor's appointments/{d_id}")
def doctor_appointments(d_id:int,db:Session=Depends(get_db)):
    p_id=session.query(Appointments.p_id).filter(Appointments.d_id==d_id).all()
    appointment_details={"patient_details":[],"status":[]}
    pat_details=db.query(User).filter(User.p_id==p_id).all()
    status=session.query(Appointments.status).filter(Appointments.d_id==d_id).all()
    appointment_count=len(p_id)
    for i in range(appointment_count):
        appointment_details["patient_details"].append(pat_details[i])
        appointment_details["status"].append(status[i])    
    return appointment_details

@auth_router.get("/patient details/{p_id}")
def patient_details(p_id:int,db:Session=Depends(get_db)):
    patient=db.query(User).filter(User.p_id==p_id).all()
    return patient

@auth_router.post("/send_appointment_details/{d_id}/{p_id}")
async def send_details_appointment(d_id:int,p_id:int,date:datetime,db:Session=Depends(get_db)):
    status=session.query(Appointments.status).filter(Appointments.p_id==p_id).filter(Appointments.d_id==d_id).first()
    email=session.query(Credentials.email).filter(Credentials.p_id==p_id).first()
    
    if status==1:
        message = MessageSchema(
            subject="Consult Meeting Details Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="please join the meeting using the given link: "+str("https://video-chat-app-gus.herokuapp.com/c5d1a684-1aa0-40fb-92ee-75d489927914")+" your date and timings are  "+str(date) 
            )
        fm = FastMail(conf)
        
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "meet invitation details has been sent"})
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error in sending appointment details")