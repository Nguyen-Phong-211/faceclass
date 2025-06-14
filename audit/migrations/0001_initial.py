# Generated by Django 5.2.2 on 2025-06-08 08:56

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceRecognitionLog',
            fields=[
                ('face_recognition_log_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('student', models.CharField(max_length=255)),
                ('face_embedding', models.BinaryField()),
                ('face_image_url', models.TextField()),
                ('confidence_score', models.DecimalField(decimal_places=5, max_digits=10)),
                ('note', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.attendance')),
            ],
            options={
                'verbose_name': 'Face Recognition Log',
                'verbose_name_plural': 'Face Recognition Logs',
                'db_table': 'face_recognition_logs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('log_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('operation', models.CharField(max_length=1)),
                ('old_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('new_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(max_length=255)),
                ('user_agent', models.CharField(max_length=255)),
                ('record_id', models.CharField(max_length=255)),
                ('entity_id', models.CharField(max_length=255)),
                ('entity_name', models.CharField(max_length=255)),
                ('action_description', models.TextField(null=True)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Audit Log',
                'verbose_name_plural': 'Audit Logs',
                'db_table': 'audit_logs',
                'managed': True,
                'indexes': [models.Index(fields=['changed_by'], name='audit_logs_changed_310180_idx')],
            },
        ),
    ]
