from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.Serializer):
    # 1. Read-Only Fields
    id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    # 2. Writable Fields
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    category = serializers.CharField(required=False, allow_blank=True)
    dead_line = serializers.DateTimeField()
    estimated_duration = serializers.FloatField(required=False, default=0.0)
    
    # 3. Status Fields (Syncs with the UI cycle button)
    status = serializers.CharField(required=False, default="Pending")
    is_completed = serializers.BooleanField(required=False, default=False)
    
    # --- THE 5-PILLAR NEURO ENGINE METADATA ---
    cognitive_score = serializers.FloatField(required=False, default=1.0)
    procrastination_risk = serializers.FloatField(required=False, default=1.0)
    reschedule_count = serializers.IntegerField(required=False, default=0)

    # 4. Create Logic
    def create(self, validated_data):
        # Explicitly ensure the owner isn't lost during creation
        return Task.objects.create(**validated_data)

    # 5. Update Logic (The Fix)
    def update(self, instance, validated_data):
        """
        Explicitly map the data to the MongoEngine instance.
        This ensures fields like is_completed are updated even in PATCH requests.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Save to MongoDB
        instance.save()
        return instance