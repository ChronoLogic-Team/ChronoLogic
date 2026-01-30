class Task(Documen):
    title = StringField(required = True, max_length=200)
    description = StringField()
    category = StringField(choices = ('study', 'work', 'personal', 'shopping', 'other'), default = 'study')

    

 

