import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AbstractBaseUser 

class MongoJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        print(f"\n--- BOUNCER CHECK ---")
        print(f"1. Header Received: {auth_header}")

        if not auth_header or not auth_header.startswith('Bearer '):
            print("-> DENIED: No token sent from the desktop app!")
            print("---------------------\n")
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(f"2. Token Decoded! Payload: {payload}")
            
            user = AbstractBaseUser.objects.get(id=payload['user_id'])
            print(f"3. Access Granted to: {user.email}")
            print("---------------------\n")
            
            return (user, token)

        except Exception as e:
            print(f"-> DENIED: Token crashed the system -> {e}")
            print("---------------------\n")
            raise AuthenticationFailed('Invalid authentication token.')