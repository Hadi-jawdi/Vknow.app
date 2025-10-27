from django.shortcuts import render
from courses_app.models import Courses


def home(request):
    courses = Courses.objects.all()
    contexts = {
        'courses':courses
    }
    return render(request, 'index.html', contexts)