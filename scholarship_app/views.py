from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .services import search_scholarships, get_popular_scholarships


class ScholarshipPageView(View):
    def get(self, request):
        popular = get_popular_scholarships()
        return render(request, 'scholarship_app/scholarship.html', {
            'popular_scholarships': popular
        })


class ScholarshipSearchAPIView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({'error': 'کوئری خالی است'}, status=400)

        results = search_scholarships(query)
        print("this is the results", results)
        return JsonResponse({'results': results})