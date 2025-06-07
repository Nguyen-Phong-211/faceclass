from django.db import models
import random
import string

def generate_random_code():
    length = random.randint(10, 20) 
    return ''.join(str(random.randint(0,9)) for _ in range(length))

class AcademicYear(models.Model):
    academic_year_id = models.BigAutoField(primary_key=True)
    academic_year_name = models.CharField(max_length=255)
    academic_year_code = models.CharField(max_length=20, default=generate_random_code, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'academic_years'
        managed = True
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'

    def __str__(self):
        return self.academic_year_name

class Subject(models.Model):
    subject_id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default='1')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=20, default=generate_random_code, unique=True)
    theoretical_credits = models.IntegerField()
    practical_credits = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subjects'
        indexes = [
            models.Index(fields=['department_id']),
            models.Index(fields=['academic_year_id']),
        ]
        managed = True
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.subject_name

class Semester(models.Model):
    semester_id = models.BigAutoField(primary_key=True)
    semester_name = models.CharField(max_length=255)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    status = models.CharField(max_length=1, default='1')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'semesters'
        indexes = [
            models.Index(fields=['academic_year_id']),
        ]
        managed = True
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def __str__(self):
        return self.semester_name
