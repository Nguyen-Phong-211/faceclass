from rest_framework import serializers
from students.models import Major

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['major_id', 'major_name', 'department']