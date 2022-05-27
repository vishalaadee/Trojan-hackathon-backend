from fastapi import FastAPI
from model_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

origins = ["*"]



from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

app=FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
