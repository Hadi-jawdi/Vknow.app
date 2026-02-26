from django.urls import path

from .import views

app_name = 'scholarship_app'

urlpatterns = [
    path("", views.scholarship, name = 'scholarship')
]