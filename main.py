from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import user_pydantic , user_pydanticIn , User
from typing import List
from fastapi import BackgroundTasks, FastAPI , Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from authentication import *
from models import *
from jose import jwt ,JWTError


app=FastAPI()


oauth_scheme=OAuth2PasswordBearer(tokenUrl="token")

@app.post('/token')
async def generate_token(request_form:OAuth2PasswordRequestForm = Depends()):
    token = await token_generate(request_form.username,request_form.password)
    return {"access_token":token , "token-type":"bearer"}


async def get_current_user(token: str = Depends(oauth_scheme)):
    try:
        payload=jwt.decode(token,credential['SECRET'],algorithms='HS256')
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
    return await user
    



@app.post('/user/me')
async def login(user_info:user_pydanticIn = Depends(get_current_user)):
    
    
    
    return {"status":"ok","response": user_info}



    




@app.get('/user')
async def user(user:user_pydanticIn):
    return{}



@app.post('/create-user')
async def createUser(user_info:user_pydanticIn):
    user_info=user_info.dict(exclude_unset=True)
    user_info['password'] = get_hash_password(user_info['password'])
    user_obj=await User.create(**user_info)
    response= await user_pydantic.from_tortoise_orm(user_obj)
    return {"status":"ok","response":response}



@app.get('/get-users')
async def get_users():
    response=await user_pydantic.from_queryset(User.all())
    return {'status':'ok','data':response}


@app.get('/user/{user_id}')
async def get_specific_user(user_id:int):
    response= await user_pydantic.from_queryset_single(User.get(id=user_id))
    return {"status":"ok","data":response}


@app.put('/user-update/{user_id}')
async def update_user(user_id:int,info:user_pydanticIn):
    user= await User.get(id=user_id)
    info=info.dict(exclude_unset=True)
    user.name=info['name']
    user.email=info['email']
    await user.save()
    response=await user_pydantic.from_tortoise_orm(user)
    return {"status":"ok","response":response}
    


@app.delete('/user-delete/{user_id}')
async def delete_specific_usesr(user_id:int):
    user_obj= await User.get(id=user_id)
    await user_obj.delete()
    return {"status":"ok"}
    

@app.delete('/all-user-delete/')
async def delete_specific_usesr():
    await User.all().delete()
    
    return {"status":"ok"}
    



class EmailSchema(BaseModel):
    email: List[EmailStr]


credential=dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = credential['EMAIL'],
    MAIL_PASSWORD = credential['PASSWORD'],
    MAIL_FROM = credential['EMAIL'],
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



html = """
<p>Thanks for using Fastapi-mail</p> 
"""


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:


    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients="a.kousha@yahoo.com",
        body=html,
        subtype="html")

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status":"ok"}





register_tortoise(app,
                  db_url="sqlite://database.sqlite3",
                  modules={"models":["models"]},
                  generate_schemas=True,
                  add_exception_handlers=True)


