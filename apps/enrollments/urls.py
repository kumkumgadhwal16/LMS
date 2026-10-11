from django.urls import path
from .views import my_courses

urlpatterns = [
    path("my-courses/", my_courses, name="my_courses"),
]