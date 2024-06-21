from mongoengine import StringField, IntField, ListField, DictField, ImageField
from Database import BaseModel

class User(BaseModel):
    id = StringField(primary_key=True)
    username = StringField(max_length=255)
    role = StringField(max_length=20)
    email = StringField(max_length=255)
    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    phone = StringField(max_length=15)
    profile_picture = ImageField()

class Group(BaseModel):
    name = StringField(max_length=255)
    permission = DictField()