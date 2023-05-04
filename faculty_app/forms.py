from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Faculty, DEPARTMENTS, SUBJECTS, Leave
from datetime import date
import datetime

class FacultyForm(UserCreationForm):
    emp_id = forms.CharField()
    department = forms.ChoiceField(choices=DEPARTMENTS, widget=forms.Select(attrs={'id': 'department'}))
    subject = forms.ChoiceField(choices=SUBJECTS, widget=forms.Select(attrs={'id': 'subject'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': '2001-01-01'}))
    date_of_join = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': str(date.today())}))

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


class LeaveApplicationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')}))
    reason = forms.CharField(max_length=200)
    class Meta:
        model = Leave
        fields = [ 'start_date', 'end_date', 'reason']


class FeedbackForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Type your feedback here...'}))


class ConfigForm(forms.Form):
    specific_latitude = forms.FloatField(label='Specific Latitude')
    specific_longitude = forms.FloatField(label='Specific Longitude')