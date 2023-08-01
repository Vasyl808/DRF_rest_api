from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Lesson
        fields = "__all__"
