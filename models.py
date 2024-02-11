from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id=fields.IntField(pk=True)
    username=fields.CharField(max_length=20)
    password=fields.CharField(max_length=80)
    email=fields.CharField(max_length=50)
    



user_pydantic=pydantic_model_creator(User,name="User")
user_pydanticIn=pydantic_model_creator(User,name="UserIn",exclude_readonly=True)