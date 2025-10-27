from django.contrib import admin

from .models import Courses,CourseLesson 
# Option 1: Basic registration
admin.site.register(Courses)
admin.site.register(CourseLesson)
