from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITH = os.getenv("ALGORITH")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # type: ignore


app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from src.routes.auth_routes import auth_router
from src.routes.account_routes import account_router
from src.routes.transaction_routes import transaction_router

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)




"""

uvicorn main:app --reload

"""
