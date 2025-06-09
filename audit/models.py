from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from accounts.models import Account
from attendance.models import Attendance

class AuditLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    operation = models.CharField(max_length=1)
    old_data = models.JSONField(encoder=DjangoJSONEncoder)
    new_data = models.JSONField(encoder=DjangoJSONEncoder)
    changed_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    record_id = models.CharField(max_length=255)
    entity_id = models.CharField(max_length=255)
    entity_name = models.CharField(max_length=255)
    action_description = models.TextField(null=True)

    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['changed_by']),
        ]
        managed = True
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return self.operation

class FaceRecognitionLog(models.Model):
    face_recognition_log_id = models.BigAutoField(primary_key=True)
    student = models.CharField(max_length=255)
    face_embedding = models.BinaryField()
    face_image_url = models.TextField()
    confidence_score = models.DecimalField(max_digits=10, decimal_places=5)
    attendace = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    note = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'face_recognition_logs'
        managed = True
        verbose_name = 'Face Recognition Log'
        verbose_name_plural = 'Face Recognition Logs'

    def __str__(self):
        return self.student_id
    