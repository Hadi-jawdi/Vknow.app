from django.shortcuts import render

# Create your views here.



def scholarship(request):
    return render(request, 'scholarship_app/scholarship.html')
