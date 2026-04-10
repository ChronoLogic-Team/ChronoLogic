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
from .authentication import MongoJWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import BasePermission

class IsMongoAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False
            
        is_anon = getattr(request.user, 'is_anonymous', False)
        return not is_anon

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsMongoAuthenticated] 
    
    def get_queryset(self):
        # THE FIX: Safely check for the nametag without crashing
        is_anon = getattr(self.request.user, 'is_anonymous', False)
        
        if is_anon:
            return Task.objects.none()
            
        return Task.objects.filter(owner=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # THE NEW INTERCEPTOR
    def perform_update(self, serializer):
        # Check if the deadline is being changed
        if 'dead_line' in serializer.validated_data:
            new_deadline = serializer.validated_data['dead_line']
            old_deadline = serializer.instance.dead_line
            
            # If the dates don't match, they rescheduled it! Add +1.
            if old_deadline and new_deadline != old_deadline:
                current_count = getattr(serializer.instance, 'reschedule_count', 0)
                serializer.save(reschedule_count=current_count + 1)
                return
                
        # Otherwise, just save normally
        serializer.save()

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
       
