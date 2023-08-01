from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Student, Teacher, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data['password']
        hashed_password = make_password(password)
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data['username'],
            password=hashed_password,
            city=validated_data.get('city'),
            address=validated_data.get('address'),
            phone=validated_data.get('phone'),
            is_staff=validated_data.get('is_staff', False),
            is_active=validated_data.get('is_active', True),
            is_student=validated_data.get('is_student', False),
            is_teacher=validated_data.get('is_teacher', False)
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            instance.password = hashed_password
        return super().update(instance, validated_data)


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # або перерахуйте тільки ті поля, які ви хочете дозволити оновлювати
        extra_kwargs = {
            'password': {'required': False},
            # додайте інші поля, які необхідно дозволити оновлювати без обов'язковості
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            instance.password = hashed_password
        return super().update(instance, validated_data)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
