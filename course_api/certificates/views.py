from django.shortcuts import render
from rest_framework import viewsets

from .models import Certificate
from .permissions import IsAdminOrTeacherOrReadOnly
from .serializers import CertificateSerializer


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = (IsAdminOrTeacherOrReadOnly, )


