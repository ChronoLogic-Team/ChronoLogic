from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    category = serializers.CharField(required=False, allow_blank=True)
    dead_line = serializers.DateTimeField()
    estimated_duration = serializers.FloatField(required=False, default=0.0)

    status = serializers.CharField(required=False, default="Pending")
    is_completed = serializers.BooleanField(required=False, default=False)

    cognitive_score = serializers.FloatField(required=False, default=1.0)
    procrastination_risk = serializers.FloatField(required=False, default=1.0)
    reschedule_count = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data):

        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance