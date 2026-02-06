from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField
import datetime

class Task(Document):
    # Core Data
    title = StringField(required=True, max_length=200)
    category = StringField(choices=('Study', 'Work', 'Health', 'Social'), default='Study')
    
    # Neuro-Symbolic Scheduling Fields
    deadline = DateTimeField(required=True)
    estimated_duration = FloatField(required=True) 
    ai_confidence_score = FloatField(default=0.0)
    
    # Status
    is_completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title