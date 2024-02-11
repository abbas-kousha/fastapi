from passlib.context import CryptContext
from models import *
from fastapi import HTTPException ,status 
from dotenv import dotenv_values
from jose import jwt

credential=dotenv_values(".env")
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")



def get_hash_password(password):
    return pwd_context.hash(password)



def verify_password(clear_password,hash_password):
    return pwd_context.verify(clear_password,hash_password)


async def authenticate_user(username,password ):
    user = await User.get(username=username)

    if user and verify_password(password, user.password):
        return user
    return False



async def token_generate(username,password):
    user = await authenticate_user(username=username, password=password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail= "invalid user or password" , headers={"WWW-Authenticate": "Bearer"})
    

    token_data={
        "id": user.id,
        "username": user.username
    }

    return jwt.encode(token_data,credential['SECRET'],algorithm='HS256')