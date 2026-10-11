from django.contrib import admin
from .models import Course, Module, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "price", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order")
    search_fields = ("title",)    




@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "lesson",
        "is_completed",
        "completed_at",
    )

    list_filter = ("is_completed",)
    search_fields = ("student__username", "lesson__title")


