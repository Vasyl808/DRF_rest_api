"""
URL configuration for course_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from courses.views import *
from certificates.views import *
from lessons.views import *
from orders.views import *
from users.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename="course")
router.register(r'user', UserViewSet)
router.register(r'student', StudentViewSet)
router.register(r'teacher', TeacherViewSet)
router.register(r'certificate', CertificateViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/lesson/', LessonAPIList.as_view()),
    path('api/v1/lesson/<int:pk>', LessonAPIDetailView.as_view()),
    path('api/v1/category/', CategoryAPIList.as_view()),
    path('api/v1/category/<int:pk>', CategoryAPIDetailView.as_view()),
    path('api/v1/course/<int:pk>/lessons/', get_course_lessons),
    path('api/v1/course/<int:pk>/author', add_author),
    path('api/v1/course/<int:pk>/add_to_wishlist', WishListAPI.as_view()),
    path('api/v1/course/<int:pk>/add_to_cart', CartAPI.as_view()),
]
