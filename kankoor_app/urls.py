from django.urls import path
from .views import test

app_name = 'kankoor_app'
urlpatterns =[
    path("test/",test, name='kankoor_test'),
]