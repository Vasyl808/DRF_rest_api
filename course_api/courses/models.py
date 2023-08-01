from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return str(self.name)


class Course(models.Model):
    LEVEL_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    count = models.IntegerField(null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, null=False)
    image_url = models.CharField(max_length=255, null=False)
    is_ended = models.BooleanField(default=False, null=False)
    is_open = models.BooleanField(default=False, null=False)
    categories = models.ManyToManyField(Category, blank=True)
    authors = models.ManyToManyField("users.Teacher", related_name='courses_authored')
    participants = models.ManyToManyField("users.Student", blank=True, related_name='courses_enrolled')

    def __str__(self) -> str:
        return str(self.name)

