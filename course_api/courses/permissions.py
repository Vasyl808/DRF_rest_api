from rest_framework import permissions

from .models import Course
from certificates.models import Certificate
from lessons.models import Lesson
from orders.models import Order
from users.models import Student, Teacher
from users.models import User
from lessons.permissions import IsAdminOrTeacherOrParticipant


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool((request.user and request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool((request.user and request.user.is_staff))


class IsAdminOrTeacherOrReadOnlyCourse(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user) == "AnonymousUser" and request.method not in permissions.SAFE_METHODS:
            return False

        if request.user.is_teacher:
            if request.method == "POST":
                return True
            teacher = Teacher.objects.get(user=request.user.pk)
            course_id = view.kwargs.get('pk')
            if not course_id:
                return bool(request.user and request.user.is_staff)
            course = Course.objects.get(pk=course_id)
            return bool(teacher in course.authors.all())

        if request.user.is_student:
            if request.method in permissions.SAFE_METHODS:
                student = Student.objects.get(user=request.user.pk)
                course_id = view.kwargs.get('pk')
                if not course_id:
                    return bool(request.user and request.user.is_staff)
                course = Course.objects.get(pk=course_id)
                return bool(student in course.participants.all())
            else:
                return False

        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(request.user) == "AnonymousUser" and request.method not in permissions.SAFE_METHODS:
            return False

        if request.user.is_teacher:
            teacher = Teacher.objects.get(user=request.user.pk)
            course = obj
            return bool(teacher in course.authors.all())

        if request.user.is_student:
            if request.method in permissions.SAFE_METHODS:
                student = Student.objects.get(user=request.user.pk)
                course = obj
                return bool(student in course.participants.all())
            else:
                return False

        return bool(request.user and request.user.is_staff)


class IsAdminOrTeacherOrParticipantCourse(IsAdminOrTeacherOrParticipant):
    def check_teacher_permission(self, teacher, view, user) -> bool:
        course_id = view.kwargs.get('pk')
        if not course_id:
            return bool(user and user.is_staff)
        course = Course.objects.get(pk=course_id).course
        return bool(teacher in course.authors.all())

    def check_student_permission(self, student, view, user) -> bool:
        course_id = view.kwargs.get('pk')
        if not course_id:
            return bool(user and user.is_staff)
        course = Course.objects.get(pk=course_id)
        return bool(student in course.participants.all())


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.method == "POST" and request.user.is_authenticated and request.user.is_teacher:
            course_id = view.kwargs.get('pk')
            if not course_id:
                return bool(request.user and request.user.is_staff)
            course = Course.objects.get(pk=course_id)
            teacher = Teacher.objects.get(user=request.user.pk)
            return bool(teacher in course.authors.all())


class IsAdminOrStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST" and request.user.is_student and request.user.is_authenticated:
            return True

        if request.method == "DELETE" and request.user.is_student and request.user.is_authenticated:
            return True
