from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import FacultyForm, LoginForm
from .models import Faculty

def register(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty = Faculty.objects.create(
                user=user,
                emp_id=form.cleaned_data['emp_id'],
                dob=form.cleaned_data['dob'],
                department=form.cleaned_data['department'],
                date_of_join=form.cleaned_data['date_of_join'],
                subject = form.cleaned_data['subject']
            )
            login(request, user)
            return redirect('index')
    else:
        form = FacultyForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def leave(request):
    return render(request, 'leave.html')

def leave_application(request):
    return render(request, 'leave_application.html')

def leave_status(request):
    return render(request, 'leave_status.html')

def profile(request):
    faculty = Faculty.objects.get(user=request.user)
    return render(request, 'profile.html', {'faculty': faculty})

def attendance(request):
    faculty = Faculty.objects.get(user=request.user)
    return render(request, 'attendance.html', {'faculty': faculty})


