from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import FacultyForm, LoginForm, LeaveApplicationForm, FeedbackForm
from .models import Faculty, Leave, Feedback, Attendance
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .decorators import user_required, admin_required
from .utils import distance
from datetime import datetime, date
from . import config
from .forms import ConfigForm



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

@user_required
def index(request):
    return render(request, 'other/index.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@user_required
def leave_management(request):
    return render(request, 'leave/leave_management.html')

@user_required
def leave_application(request):
    return render(request, 'leave/leave_application.html')

@user_required
def delete_leave(request, leave_id):
    leave = Leave.objects.get(pk=leave_id)
    if leave.user == request.user:
        leave.delete()
    return redirect('leave_status')

def leave_status(request):
    user_leaves = Leave.objects.filter(user=request.user)
    return render(request, 'leave/leave_status.html', {'user_leaves': user_leaves})

@user_required
def profile(request):
    faculty = Faculty.objects.get(user=request.user)
    return render(request, 'other/profile.html', {'faculty': faculty})

@user_required
def attendance(request):
    faculty = Faculty.objects.get(user=request.user)
    return render(request, 'attendance/attendance.html', {'faculty': faculty})


@user_required
def leave_application(request):
    form = LeaveApplicationForm(request.POST or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.user = request.user
        leave.save()
        return redirect('leave_status')
    context = {'form': form}
    return render(request, 'leave/leave_application.html', context)

@user_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(user=request.user, message=form.cleaned_data['message'])
            feedback.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form})

def home(request):
    return render(request, 'other/home.html')

def feedback_success(request):
    return render(request, 'feedback/feedback_success.html')

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'
    success_url = reverse_lazy('admin_home')

    def get_success_url(self):
        return self.success_url

@admin_required
def admin_home(request):
    users = User.objects.all()
    return render(request, 'admin/admin_home.html', {'users': users})

def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

@admin_required
def admin_leave(request):
    leaves = Leave.objects.select_related('user__faculty').all()
    return render(request, 'admin/admin_leave.html', {'leaves': leaves})

def update_status(request, leave_id):
    leave = Leave.objects.get(id=leave_id)
    status = request.POST.get('status')

    if status == 'approved':
        leave.status = 'approved'
    elif status == 'declined':
        leave.status = 'declined'

    leave.save()
    leaves = Leave.objects.all()
    return render(request, 'admin/admin_leave.html', {'leaves': leaves})

@admin_required
def admin_feedback(request):
    feedbacks = Feedback.objects.select_related('user').all().exclude(user__is_superuser=True)
    non_admin_feedbacks = feedbacks.filter(user__in=User.objects.filter(is_superuser=False))
    return render(request, 'admin/admin_feedback.html', {'feedbacks': non_admin_feedbacks})

def mark_attendance(request):
    user = request.user
    today = date.today()
    attendance_exists = Attendance.objects.filter(user=user, mark_date=today).exists()
    if attendance_exists:
        return render(request, 'attendance/marked.html', {'message': 'Attendance already marked for today!'})
    
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        
        specific_lat = config.SPECIFIC_LATITUDE
        specific_lng = config.SPECIFIC_LONGITUDE
        dist = distance(lat, lng, specific_lat, specific_lng)
        if dist < 1:
            now = datetime.now().time()
            attendance = Attendance(user=user, mark_date=today, mark_time=now, status=True)
            attendance.save()
            return render(request, 'attendance/mark_attendance.html', {'message': 'Attendance marked successfully!'})
        else:
            return render(request, 'attendance/mark_attendance.html', {'message': 'You are not at the designated location!'})
    return render(request, 'attendance/mark_attendance.html')

def view_attendance(request):
    faculty = Faculty.objects.get(user=request.user)
    attendances = Attendance.objects.filter(user=request.user)
    return render(request, 'attendance/view_attendance.html', {'attendances': attendances, 'faculty':faculty})

@admin_required
def admin_view_attendance(request):
     faculty = Faculty.objects.select_related('user').exclude(user__is_superuser=True)
     attendances = Attendance.objects.select_related('user').exclude(user__is_superuser=True)
     return render(request, 'admin/admin_view_attendance.html', {'attendances': attendances, 'faculty':faculty})

@admin_required
def admin_config(request):
    form = ConfigForm(initial={'specific_latitude': config.SPECIFIC_LATITUDE,
                               'specific_longitude': config.SPECIFIC_LONGITUDE})
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            config.SPECIFIC_LATITUDE = form.cleaned_data['specific_latitude']
            config.SPECIFIC_LONGITUDE = form.cleaned_data['specific_longitude']
            return render(request, 'admin/admin_success.html')
    return render(request, 'admin/admin_config.html', {'form': form})


