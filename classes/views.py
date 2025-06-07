from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from students.models import Department
from students.serializers import DepartmentSerializer
from .models import Class
from .serializers import ClassSerializer

@api_view(['GET'])
def get_departments(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_classes_by_department(request, department_id):
    classes = Class.objects.filter(department_id=department_id)
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)
