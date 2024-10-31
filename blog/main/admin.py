from django.contrib import admin
from .models import Category, Course, Section, Lesson, Enrollment
from django.contrib.auth.models import User
# Register your models here.


from django.contrib import admin
from .models import Category, Course, Section, Lesson, Enrollment, Comment, Rating
from .views import send_update_email, update_course

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'instructor', 'created_at')
#     search_fields = ('title', 'instructor__username')
#     list_filter = ('category',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'order')
    list_display_links = ('id', 'title', 'course',)
    search_fields = ('title',)
    list_filter = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'section', 'order', 'video')
    search_fields = ('title',)
    list_filter = ('section',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')


class CourseAdmin(admin.ModelAdmin):
    # ... boshqa admin sozlamalari

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:  # Agar kurs yangilanayotgan bo'lsa
            update_course(obj)  # Yangilanishlar bilan bog'liq email yuborish

admin.site.register(Course, CourseAdmin)

admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'comment', 'created_at')
    search_fields = ('user__username', 'lesson__title')
    list_display_links = ('id', 'user')



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'rating', 'created_at')
    list_display_links = ('id', 'user')