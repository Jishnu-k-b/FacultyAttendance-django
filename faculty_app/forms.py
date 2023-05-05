from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import  DEPARTMENTS, SUBJECTS, Leave, Faculty
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
    def clean_emp_id(self):
        emp_id = self.cleaned_data['emp_id']
        if Faculty.objects.filter(emp_id=emp_id).exists():
            raise forms.ValidationError("This emp_id is already in use. Please use a different emp_id.")
        return emp_id
    


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                self.add_error('username', 'Invalid username or password.')


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