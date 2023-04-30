from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('leave_management/', views.leave_management, name='leave_management'),
    path('leave_application/', views.leave_application, name='leave_application'),
    path('leave_status/', views.leave_status, name='leave_status'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin_login/', views.CustomAdminLoginView.as_view(), name='admin_login'),
    path('admin_home/',views.admin_home, name='admin_home'),
]
