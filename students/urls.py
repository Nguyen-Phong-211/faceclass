from django.urls import path
from .views import CreateStudentView

urlpatterns = [
    path('api/students/', CreateStudentView.as_view(), name='create_student'),
]