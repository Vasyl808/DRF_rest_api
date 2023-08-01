from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.username)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='student_profile')
    certificates = models.ManyToManyField("certificates.Certificate", blank=True, related_name='student_certificates')
    wishlist = models.ManyToManyField('courses.Course', blank=True, related_name='wishlist_students')
    cart = models.ManyToManyField('courses.Course', blank=True, related_name='cart_students')

    def __str__(self) -> str:
        return str(self.user.username)


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='teacher_profile')
    description = models.CharField(max_length=255, null=False)
    experience = models.FloatField(null=False)
    diploma_url = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return str(self.user.username)
