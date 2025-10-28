from django.urls import path
from . import views

app_name = "upload_book_app"

urlpatterns = [
    
    
# New resource routes
    path("", views.upload_book, name="resources"),
    

]