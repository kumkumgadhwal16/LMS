from django.urls import path
from .views import course_list,course_detail,enroll_course,lesson_detail
from .views import mark_lesson_complete,create_course,publish_course


urlpatterns = [
    path("", course_list, name="course_list"),
    path("<int:id>/", course_detail, name="course_detail"),
    path("<int:id>/enroll/", enroll_course, name="enroll_course"),
     path("lessons/<int:lesson_id>/",lesson_detail,
             name="lesson_detail"),
    path(
    "lessons/<int:lesson_id>/complete/",
    mark_lesson_complete,
    name="mark_lesson_complete"

    
), 

   path("create/", create_course, name="create_course"),

   path(
    "<int:course_id>/publish/",
    publish_course,
    name="publish_course"
),
  
   
]