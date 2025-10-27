from django.urls import path
from . import views

app_name = 'account_app'


urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),

]
