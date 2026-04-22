import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from api.models import AbstractBaseUser

def create_admin():
    email = "waliur@email.com"
    password = "1234"

    AbstractBaseUser.objects.filter(email=email).delete()

    user = AbstractBaseUser(
        email=email,
        full_name="Md.Waliur Rahman",
        password=make_password(password),
        is_inactive=False
    )
    user.save()

    print(f"SUCCESS: User {email} was created in MongoDB!")

if __name__ == "__main__":
    create_admin()