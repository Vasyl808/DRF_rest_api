from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import generics, viewsets
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import *
from .permissions import *
from .serializers import *
from certificates.models import Certificate
from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from orders.models import Order
from users.serializers import UserSerializer
from users.models import Student, Teacher, User


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrTeacherOrReadOnlyCourse, )

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Course.objects.all()

        return Course.objects.filter(pk=pk)

    @action(methods=['get'], detail=False)
    def categories(self, request):
        categories = Category.objects.all()
        return Response({"categories": [category for category in CategorySerializer(categories, many=True).data]})

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response(status=404, data={"error": "Not found"})
        return Response({"category": CategorySerializer(category).data})


class CategoryAPIList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class CategoryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


@api_view(["GET"])
@permission_classes([IsAdminOrTeacherOrParticipantCourse])
def get_course_lessons(request, pk):
    if not pk:
        return Response(status=404, data={"error": "Not found"})

    try:
        course = Course.objects.get(pk=pk)
        lessons = Lesson.objects.filter(course=course)
    except:
        return Response(status=404, data={"error": "Not found"})

    return Response({"lessons": [lesson for lesson in LessonSerializer(lessons, many=True).data]})


@api_view(["POST"])
@permission_classes([IsAdminOrOwnerOrReadOnly])
def add_author(request, pk):
    user_id = request.data.get("user_id")

    if not pk:
        return Response(status=404, data={"error": "Not found"})

    try:
        course = Course.objects.get(pk=pk)
    except:
        return Response(status=404, data={"error": "Not course found"})

    try:
        user = User.objects.get(pk=user_id)
        if user.is_teacher or user.is_staff:
            teacher = Teacher.objects.get(user=user_id)
            if teacher not in course.authors.all():
                course.authors.add(teacher)
                course.save()
            else:
                return Response(status=400, data={"error": "This teacher already in authors"})
    except:
        return Response(status=404, data={"error": "Something were wrong"})

    return Response(CourseSerializer(course))

