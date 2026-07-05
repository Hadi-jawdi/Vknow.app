from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View


from django.shortcuts import render
from django.views import View
from django.db.models import Q
from .models import Scholarship

class ScholarshipPageView(View):
    def get(self, request):
        scholarships = Scholarship.objects.filter(is_active=True)
        return render(request, 'scholarship_app/scholarship.html', {
            'scholarships': scholarships
        })

