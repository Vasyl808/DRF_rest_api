from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lesson
from .permissions import IsAdminOrTeacherOrParticipantLesson
from .serializers import LessonSerializer


class LessonAPIDetailView(APIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAdminOrTeacherOrParticipantLesson, )

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method GET not allowed"})
        try:
            lesson = Lesson.objects.get(pk=pk)
        except:
            return Response(status=404, data={"error": "Not found"})
        return Response(LessonSerializer(lesson).data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Lesson.objects.get(pk=pk)
        except:
            return Response(status=404, data={"error": "Not found"})

        serializer = LessonSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"lesson": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Lesson.objects.get(pk=pk)
        except:
            return Response(status=404, data={"error": "Not found"})

        try:
            instance.delete()
        except:
            return Response(status=400, data={"error": "Something were wrong"})

        return Response({"lesson": "delete lesson" + str(pk)})


class LessonAPIList(APIView):
    permission_classes = (IsAdminOrTeacherOrParticipantLesson,)
    serializer_class = LessonSerializer

    def get(self, request):
        lessons = Lesson.objects.all()
        return Response({"lessons": LessonSerializer(lessons, many=True).data})

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"lesson": serializer.data})
