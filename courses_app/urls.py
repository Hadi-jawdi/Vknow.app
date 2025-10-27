
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('all_lessons/', views.show_all_lessons, name='show_all_lessons'),

    
]