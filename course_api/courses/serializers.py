from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Course, Category
from certificates.models import Certificate
from lessons.models import Lesson
from orders.models import Order
from users.models import Student, Teacher
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["name", "description", "price", "count", "start_time", "end_time",
                  "level", "image_url", "is_ended", "is_open", "categories", "authors", "participants"]


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
