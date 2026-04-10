import django.db.models.fields.reverse_related
from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField, ReferenceField, IntField
import datetime


class AbstractBaseUser(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    full_name = StringField(required=True)
    is_inactive = BooleanField(default=True)


class Task(Document):
    # core data
    title = StringField(required=True, max_length=200)
    description = StringField()
    category = StringField(choices=('study', 'work', 'personal', 'shopping', 'other'), default='study')

    # Scheduling
    dead_line = DateTimeField(required=True)
    estimated_duration = FloatField(required=True)
    actual_duration = FloatField(default=0.0)

    # Status
    is_completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    # AI Metadata (For the "Neuro-Symbolic" part)
    ai_confidence_score = FloatField(default=0.0)

    # AI Metadata (For the "Neuro-Symbolic" part)
    ai_confidence_score = FloatField(default=0.0)
    reschedule_count = IntField(default=0) # THE NEW FIELD!

    owner = ReferenceField(AbstractBaseUser, required=True, reverse_delete_rule='CASCADE')
    
    def __str__(self):
        return self.title
