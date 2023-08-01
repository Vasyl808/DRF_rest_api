from rest_framework import permissions

from courses.models import Course
from certificates.models import Certificate
from lessons.models import Lesson
from orders.models import Order
from .models import Student, Teacher
from .models import User


class IsAdminOrOwnerOrReadOnlyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_superuser or request.user == obj)


class IsAdminOrOwnerOrReadOnlyStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_superuser or (request.user == obj.user and request.user.is_student))


class IsAdminOrOwnerOrReadOnlyTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_superuser or (request.user == obj.user and request.user.is_teacher))
