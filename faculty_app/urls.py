from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('leave_management/', views.leave_management, name='leave_management'),
    path('leave_application/', views.leave_application, name='leave_application'),
    path('leave-status/', views.leave_status, name='leave_status'),
    path('delete-leave/<int:leave_id>/', views.delete_leave, name='delete_leave'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin_login/', views.CustomAdminLoginView.as_view(), name='admin_login'),
    path('admin_home/',views.admin_home, name='admin_home'),
    path('user_list/',views.user_list, name='user_list'),
    path('update_status/<int:leave_id>/', views.update_status, name='update_status'),
    path('admin_leave/', views.admin_leave, name='admin_leave'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin_feedback/',views.admin_feedback, name='admin_feedback'),
    path('feedback_success/',views.feedback_success, name='feedback_success'),
]
