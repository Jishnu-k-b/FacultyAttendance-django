from django.db import models
from django.contrib.auth.models import User

DEPARTMENTS = [
    ('MCA', 'Computer Application'),
    ('MBA', 'Business Administration'),
    ('BHM', 'Hotel Management'),
    ('MCOM', 'Commerce'),
]

SUBJECTS = [
    ('COS', 'CORE SUBJECT'),
    ('OPS', 'OPTIONAL SUBJECT'),
]

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty')
    dob = models.DateField()
    department = models.CharField(max_length=4, choices=DEPARTMENTS)
    date_of_join = models.DateField()
    subject = models.CharField(max_length=4, choices=SUBJECTS)
    emp_id = models.CharField(max_length=10, unique=True)
    


    def __str__(self):
        return self.user.username