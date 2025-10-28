from django.shortcuts import render



def upload_book(request):
    return render(request, "upload_book_app/pages/upload.html")


