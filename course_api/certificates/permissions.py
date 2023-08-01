from rest_framework import permissions

from courses.models import Course
from .models import Certificate
from lessons.models import Lesson
from orders.models import Order
from users.models import Student, Teacher
from users.models import User


class IsAdminOrTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user and request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user) == "AnonymousUser" and request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user) == "AnonymousUser" and request.method not in permissions.SAFE_METHODS:
            return True

        return bool((request.user and request.user.is_staff) or (request.user and request.user.is_teacher))

    def has_object_permission(self, request, view, obj):
        if request.user and request.method in permissions.SAFE_METHODS:
            return True

        return bool((request.user and request.user.is_staff))
