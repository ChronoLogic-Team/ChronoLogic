import django.db.models.fields.reverse_related
from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField, ReferenceField, IntField
import datetime

class AbstractBaseUser(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    full_name = StringField(required=True)
    is_inactive = BooleanField(default=True)

class Task(Document):
    # THE FIX: Tell MongoDB not to crash if it sees old deleted fields!
    meta = {'strict': False}
    
    # core data
    title = StringField(required=True, max_length=200)
    description = StringField()
    category = StringField(max_length=12)

    # Scheduling
    dead_line = DateTimeField(required=True)
    estimated_duration = FloatField(default=0.0)
    actual_duration = FloatField(default=0.0)

    # Status
    status = StringField(default="Pending")
    is_completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    # --- THE 5-PILLAR NEURO ENGINE METADATA ---
    cognitive_score = FloatField(default=1.0)       
    procrastination_risk = FloatField(default=1.0)  
    
    # Symbolic Metadata
    reschedule_count = IntField(default=0) 

    owner = ReferenceField(AbstractBaseUser, required=True, reverse_delete_rule='CASCADE')
    
    def __str__(self):
        return self.title