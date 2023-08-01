from rest_framework import permissions

from courses.models import Course
from certificates.models import Certificate
from .models import Lesson
from orders.models import Order
from users.models import Student, Teacher
from users.models import User


class IsAdminOrTeacherOrParticipant(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if str(request.user) == "AnonymousUser":
            return False

        if request.user.is_teacher:
            if request.method in permissions.SAFE_METHODS or request.method == "POST":
                return True
            teacher = Teacher.objects.get(user=request.user.pk)
            return self.check_teacher_permission(teacher, view, request.user)

        if request.user.is_student:
            if request.method in permissions.SAFE_METHODS:
                student = Student.objects.get(user=request.user.pk)
                return self.check_student_permission(student, view, request.user)
            else:
                return False

        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if str(request.user) == "AnonymousUser":
            return False

        if request.user.is_teacher:
            if request.method in permissions.SAFE_METHODS or request.method == "POST":
                return True
            teacher = Teacher.objects.get(user=request.user.pk)
            return self.check_teacher_permission(teacher, view, request.user)

        if request.user.is_student:
            if request.method in permissions.SAFE_METHODS:
                student = Student.objects.get(user=request.user.pk)
                return self.check_student_permission(student, view, request.user)
            else:
                return False

        return bool(request.user and request.user.is_staff)

    def check_teacher_permission(self, teacher, view, user) -> bool:
        raise NotImplementedError

    def check_student_permission(self, student, view, user) -> bool:
        raise NotImplementedError


class IsAdminOrTeacherOrParticipantLesson(IsAdminOrTeacherOrParticipant):
    def check_teacher_permission(self, teacher, view, user) -> bool:
        lesson_id = view.kwargs.get('pk')
        if not lesson_id:
            return bool(user and user.is_staff)
        course = Lesson.objects.get(pk=lesson_id).course
        return bool(teacher in course.authors.all())

    def check_student_permission(self, student, view, user) -> bool:
        lesson_id = view.kwargs.get('pk')
        if not lesson_id:
            return bool(user and user.is_staff)
        course = Lesson.objects.get(pk=lesson_id).course
        return bool(student in course.participants.all())
