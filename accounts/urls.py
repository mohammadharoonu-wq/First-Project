from django.urls import path
from .views import SignupView, LoginView, LogoutView, TeacherDashboard, StudentParentDashboard

urlpatterns = [
    # --- Authentication APIs ---
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # --- Dashboard APIs ---
    path('teacher/dashboard/', TeacherDashboard.as_view(), name='teacher_dashboard'),
    path('student/dashboard/', StudentParentDashboard.as_view(), name='student_dashboard'),
]