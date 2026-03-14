from django.shortcuts import render
from rest_framework_mongoengine import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
from django.conf import settings
from .serializers import TaskSerializer
from .models import Task, AbstractBaseUser

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('full_name')

        if AbstractBaseUser.objects(email = email).first():
            return Response({'error': 'Email exists'}) 

        hashed = make_password(password)
        user = AbstractBaseUser(email = email, password = hashed, full_name = name)
        user.save()
        return Response({'success': 'User created'})

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = AbstractBaseUser.objects(email = email).first()

        if user is None or not check_password(password, user.password):
            return Response({'error' : 'Invalid_login'})
        
        payload = {
            'user_id': str(user.id),
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token})
       
