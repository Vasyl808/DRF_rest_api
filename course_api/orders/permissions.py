from rest_framework import permissions

from courses.models import Course
from certificates.models import Certificate
from lessons.models import Lesson
from .models import Order
from users.models import Student, Teacher
from users.models import User


class IsAdminOrStudentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated and request.method == "POST":
            return True

        if request.user and request.user.is_authenticated and request.user.is_student and request.method == "POST":
            return True

        return bool((request.user and request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                if request.user.is_student and obj.user == request.user:
                    return True

                if request.user.is_student and obj.user != request.user:
                    return False

                if request.user.is_teacher:
                    return False

            if request.method == "DELETE" and obj.user == request.user:
                return True

        return bool((request.user and request.user.is_staff))
