from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Faculty, DEPARTMENTS, SUBJECTS

class FacultyForm(UserCreationForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    department = forms.ChoiceField(choices=DEPARTMENTS)
    date_of_join = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    subject = forms.ChoiceField(choices= SUBJECTS)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
