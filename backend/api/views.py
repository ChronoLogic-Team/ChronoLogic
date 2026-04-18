from django.shortcuts import render
from rest_framework_mongoengine import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
import json
from django.conf import settings

# --- AI SDK IMPORT ---
import google.generativeai as genai
# PUT YOUR ACTUAL GEMINI API KEY IN THE QUOTES BELOW:
genai.configure(api_key="AIzaSyDUWWVn8ouAOLjxMFqCCO0c0sksiVpdY4I")

from .serializers import TaskSerializer
from .models import Task, AbstractBaseUser
from .authentication import MongoJWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

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
        is_anon = getattr(self.request.user, 'is_anonymous', False)
        if is_anon:
            return Task.objects.none()
        return Task.objects.filter(owner=self.request.user)
        
    # --- THE 5-PILLAR NEURO ENGINE ---
    def perform_create(self, serializer):
        title = serializer.validated_data.get('title', 'Unknown Task')
        desc = serializer.validated_data.get('description', '')
        duration = serializer.validated_data.get('estimated_duration', 0.0)
        try:
            # 1. Smart Router
            valid_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            best_model = next((m for m in valid_models if 'flash' in m), valid_models[0])
            
            # flush=True forces Python to print to the terminal instantly
            print(f"🧠 AI Brain routing to: {best_model}", flush=True) 
            
            # Force JSON mode so the parser is bulletproof
            model = genai.GenerativeModel(best_model, generation_config={"response_mime_type": "application/json"})
            
            prompt = f"""
            Analyze task: "{title}". Description: "{desc}".
            Return a JSON object with these exact keys: "predicted_hours" (float), "category" (string max 8 chars), "cognitive_score" (float 1.0 to 3.0), "procrastination_risk" (float 1.0 to 5.0).
            """
            
            # 2. Call the AI
            response = model.generate_content(prompt)
            ai_data = json.loads(response.text)

            # 4. Extract Data & Apply Zero-UI Tricks
            ai_duration = float(ai_data.get('predicted_hours', duration))
            
            # THE FIX: Keep the category string short so PyQt's font scaler doesn't crash!
            raw_cat = str(ai_data.get('category', 'Task'))
            final_category = raw_cat[:12] # Hard limit to 12 characters

            # 5. Save to MongoDB
            serializer.save(
                owner=self.request.user,
                estimated_duration=ai_duration,
                category=final_category,
                cognitive_score=float(ai_data.get('cognitive_score', 1.0)),
                procrastination_risk=float(ai_data.get('procrastination_risk', 1.0))
            )
            print(f"🤖 AI Successfully Analyzed Task: {title}", flush=True)

        except Exception as e:
            print(f"⚠️ AI Engine Fallback. Error: {e}", flush=True) 
            serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if 'dead_line' in serializer.validated_data:
            new_deadline = serializer.validated_data['dead_line']
            old_deadline = serializer.instance.dead_line
            
            if old_deadline and new_deadline != old_deadline:
                current_count = getattr(serializer.instance, 'reschedule_count', 0)
                serializer.save(reschedule_count=current_count + 1)
                return
                
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