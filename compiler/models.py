from django.db import models
import bcrypt
from typing import Tuple, Union
import os
from dotenv import load_dotenv
import jwt
import datetime

from .errors import *
from .utils.chore import is_valid_email
from .utils.hash import hash_password, verify_password


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_MAX_TIMEDELTA = datetime.timedelta(minutes=30)

if not JWT_SECRET_KEY:
    raise("Please create an Environment Variable named JWT_SECRET_KEY")

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
 
    def __str__(self) -> str:
        return self.username

    
    @classmethod
    def create_user(cls :"User", name :str, username :str, email :str, password :str) -> Tuple[bool, Union["User", str]]:
        if not all([name, username, email, password]):
            return (False, IncompleteData)

        if User.objects.filter(username=username).exists():
            return (False, UserExists)

        if not is_valid_email(email):
            return (False, InvalidEmail)

        hashed_password = hash_password(password)
        user = cls(name=name, username=username, email=email, password_hash=hashed_password)
        user.save()

        return(True, user)
