from django.urls import path
from .views import get_departments, get_major_by_department

urlpatterns = [
    path('api/departments/', get_departments),
    path('api/majors/<int:department_id>/', get_major_by_department),
]