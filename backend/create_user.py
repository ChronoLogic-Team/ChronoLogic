# backend/create_user.py
import os
import django

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from api.models import AbstractBaseUser

def create_admin():
    email = "waliur@email.com"
    password = "1234"
    
    # 2. Clear any old attempts just in case
    AbstractBaseUser.objects.filter(email=email).delete()
    
    # 3. Create the official MongoDB document
    user = AbstractBaseUser(
        email=email,
        full_name="Md.Waliur Rahman", 
        password=make_password(password), # Hashes "1234" into a secure string
        is_inactive=False
    )
    user.save()
    
    print(f"SUCCESS: User {email} was created in MongoDB!")

if __name__ == "__main__":
    create_admin()