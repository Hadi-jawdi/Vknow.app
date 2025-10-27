from django.shortcuts import render
from courses_app.models import CourseLesson

def show_all_lessons(request):
    # Get all lessons in random order
    lessons = CourseLesson.objects.order_by('?')
    
    context = {
        'lessons': lessons
    }
    
    return render(request, "courses_app/pages/all_lessons.html", context)
