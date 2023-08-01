from django.shortcuts import render
from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminOrStudentOrReadOnly
from users.models import Student
from users.serializers import StudentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrStudentOrReadOnly, )

    def perform_create(self, serializer):
        student = Student.objects.get(user=self.request.user)
        serializer.save(user=student)
