# logdb_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #auth
    path('api/auth/register/', views.register_user, name='register'),
    path('api/auth/login/', views.login_user, name='login'),
    #project
    path('api/projects/', views.create_project, name='create_project'),
    path('api/logs/', views.view_logs, name='view_logs'),
    path('api/audit-logs/', views.view_audit_logs, name='view_audit_logs'),
    path('api/logs/submit/', views.submit_log, name='submit_log'),
]

