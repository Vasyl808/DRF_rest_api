from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from  django.shortcuts import get_object_or_404

from .models import Order
from courses.models import Course
from users.models import Student
from users.serializers import StudentSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=StudentSerializer)

    class Meta:
        model = Order
        fields = "__all__"

    def get_user(self, obj):
        return get_object_or_404(Student, user=self.context['request'].user)
