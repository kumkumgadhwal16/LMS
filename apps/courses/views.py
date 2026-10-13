from django.shortcuts import render,get_object_or_404,redirect
from .models import Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.enrollments.models import Enrollment
from .models import Course, Lesson,LessonProgress
from django.utils import timezone




def course_list(request):
    courses = Course.objects.filter(status=Course.Status.PUBLISHED)

    return render(
        request,
        "courses/course_list.html",
        {"courses": courses}
    )


def course_detail(request, id):
    course = get_object_or_404(
        Course,
        id=id,
        status=Course.Status.PUBLISHED
    )

    return render(
        request,
        "courses/course_detail.html",
        {"course": course}
    )



@login_required
def enroll_course(request, id):
    if request.method != "POST":
        return redirect("course_detail", id=id)

    course = get_object_or_404(
        Course,
        id=id,
        status=Course.Status.PUBLISHED
    )

    if request.user.role != "STUDENT":
        messages.error(request, "Only students can enroll.")
        return redirect("course_detail", id=id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if created:
        messages.success(request, "Successfully enrolled!")
    else:
        messages.info(request, "You are already enrolled.")

    return redirect("course_detail", id=id)



@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson
    )

    if request.method == "POST":
        progress.is_completed = True
        progress.save()

        messages.success(request, "Lesson completed successfully!")
        return redirect("lesson_detail", lesson_id=lesson.id)

    return render(
        request,
        "courses/lesson_detail.html",
        {
            "lesson": lesson,
            "progress": progress,
        }
    )


# @login_required
# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(
#         Lesson,
#         id=lesson_id,
#         module__course__status=Course.Status.PUBLISHED
#     )

#     # Check student enrollment
#     if request.user.role == "STUDENT":
#         is_enrolled = Enrollment.objects.filter(
#             student=request.user,
#             course=lesson.module.course
#         ).exists()

#         if not is_enrolled:
#             messages.error(
#                 request,
#                 "Please enroll in this course to access lessons."
#             )
#             return redirect(
#                 "course_detail",
#                 id=lesson.module.course.id
#             )

#     return render(
#         request,
#         "courses/lesson_detail.html",
#         {"lesson": lesson}
#     )




@login_required
def mark_lesson_complete(request, lesson_id):

    if request.method != "POST":
        return redirect("course_list")

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        module__course__status=Course.Status.PUBLISHED
    )

    if request.user.role != "STUDENT":
        messages.error(request, "Only students can complete lessons.")
        return redirect(
            "course_detail",
            id=lesson.module.course.id
        )

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=lesson.module.course
    ).exists()

    if not is_enrolled:
        messages.error(request, "Please enroll in this course first.")
        return redirect(
            "course_detail",
            id=lesson.module.course.id
        )

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson
    )

    progress.is_completed = True
    progress.completed_at = timezone.now()
    progress.save()

    messages.success(request, "Lesson marked as completed!")

    return redirect("lesson_detail", lesson_id=lesson.id)



@login_required
def create_course(request):
    # Only instructors can create courses
    if request.user.role != "INSTRUCTOR":
        messages.error(request, "Only instructors can create courses.")
        return redirect("course_list")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "0").strip()

        if title and description and price:
            try:
                price = float(price)

                if price < 0:
                    raise ValueError

                Course.objects.create(
                    title=title,
                    description=description,
                    price=price,
                    instructor=request.user,
                    status=Course.Status.DRAFT
                )

                messages.success(
                    request,
                    "Course created successfully!"
                )
                return redirect("course_list")

            except (ValueError, TypeError):
                messages.error(request, "Please enter a valid price.")
        else:
            messages.error(
                request,
                "Please fill in all required fields."
            )

    return render(request, "courses/create_course.html")




@login_required
def publish_course(request, course_id):
    if request.user.role != "INSTRUCTOR":
        messages.error(
            request,
            "Only instructors can publish courses."
        )
        return redirect("course_list")

    if request.method != "POST":
        return redirect("course_list")

    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    course.status = Course.Status.PUBLISHED
    course.save(update_fields=["status"])

    messages.success(
        request,
        "Course published successfully!"
    )

    return redirect("course_list")
