class Task(Documen):

    #core data
    title = StringField(required = True, max_length=200)
    description = StringField()
    category = StringField(choices = ('study', 'work', 'personal', 'shopping', 'other'), default = 'study')

    #Scheduling
    dead_line=DateTimeField(required = True)
    estimated_duration = FloatField(required = True )
    actual_duration = FloatField(default = 0.0)

    #Status
    is_completed = BooleanField(default = False)
    created_at = DateTimeField(default = datetime.datetime.now)

    # AI Metadata (For the "Neuro-Symbolic" part)
    ai_confidence_score = FloatField(default=0.0)

def __str__(self):
    return self.title