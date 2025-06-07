from django.db import models
import random
import string
from students.models import Department
from subjects.models import AcademicYear
from students.models import Student
from subjects.models import Subject
from rooms.models import Room
from lecturers.models import Lecturer


def generate_random_code():
    length = random.randint(10, 20) 
    return ''.join(str(random.randint(0,9)) for _ in range(length))

class Class(models.Model):
    class_id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    class Meta:
        db_table = 'classes'
        indexes = [
            models.Index(fields=['department_id']),
            models.Index(fields=['academic_year_id']),
        ]
        managed = True
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.class_name

class ClassStudent(models.Model):
    class_student_id = models.BigAutoField(primary_key=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_active = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    registration_status = models.CharField(max_length=20, default='auto')
    
    class Meta:
        db_table = 'class_students'
        indexes = [
            models.Index(fields=['class_id']),
            models.Index(fields=['student_id']),
        ]
        managed = True
        verbose_name = 'Class Student'
        verbose_name_plural = 'Class Students'

    def __str__(self):
        return f"{self.class_id} - {self.student_id}"

class Schedule(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=False)
    end_time = models.DateTimeField(auto_now_add=False)
    repeat_weekly = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        db_table = 'schedules'
        indexes = [
            models.Index(fields=['class_id']),
            models.Index(fields=['subject_id']),
            models.Index(fields=['room_id']),
        ]
        managed = True
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        return f"{self.class_id} - {self.subject_id}"

class QRCheckin(models.Model):
    qr_checkin_id = models.BigAutoField(primary_key=True)
    qr_code = models.CharField(max_length=255)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    expire_at = models.TimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    is_active = models.CharField(max_length=1)
    usage_count = models.IntegerField()
    max_usage = models.IntegerField()
    radius = models.IntegerField()
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    used_by_student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'qr_checkins'
        indexes = [
            models.Index(fields=['schedule_id']),
            models.Index(fields=['created_by']),
            models.Index(fields=['used_by_student_id']),
        ]
        managed = True
        verbose_name = 'QR Checkin'
        verbose_name_plural = 'QR Checkins'

    def __str__(self):
        return f"{self.class_id} - {self.student_id}"

