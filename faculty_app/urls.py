from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('leave/', views.leave, name='leave'),
    path('leave_application/', views.leave_application, name='leave_application'),
    path('leave_status/', views.leave_status, name='leave_status'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance')

]
