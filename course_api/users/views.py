from django.shortcuts import render
from rest_framework import viewsets

from .models import Student, Teacher, User
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer, PartialUserSerializer
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminOrOwnerOrReadOnlyUser, )

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return PartialUserSerializer
        return UserSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdminOrOwnerOrReadOnlyStudent, )


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAdminOrOwnerOrReadOnlyTeacher, )
