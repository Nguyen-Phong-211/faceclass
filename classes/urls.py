from django.urls import path
from .views import get_departments, get_classes_by_department

urlpatterns = [
    path('api/departments/', get_departments),
    path('api/classes/<int:department_id>/', get_classes_by_department),
]