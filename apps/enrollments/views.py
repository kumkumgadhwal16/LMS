from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from .models import Enrollment
from apps.courses.models import Lesson, LessonProgress


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    for enrollment in enrollments:
        total_lessons = Lesson.objects.filter(
            module__course=enrollment.course
        ).count()

        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=enrollment.course,
            is_completed=True
        ).count()

        if total_lessons > 0:
            progress = int(
                completed_lessons * 100 / total_lessons
            )
        else:
            progress = 0

        enrollment.progress_percentage = progress
        enrollment.completed_lessons = completed_lessons
        enrollment.total_lessons = total_lessons
        enrollment.is_course_completed = (
            total_lessons > 0
            and completed_lessons == total_lessons
        )

    return render(
        request,
        "enrollments/my_courses.html",
        {"enrollments": enrollments}
    )