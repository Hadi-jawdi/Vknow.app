from django.urls import path
from . import views

app_name = 'kankoor_app'

urlpatterns = [
    path('', views.kankor_home, name='kankoor_home'),
    path('start/', views.start_test, name='start_test'),
    path('submit/', views.submit_test, name='submit_test'),
]