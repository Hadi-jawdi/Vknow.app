from django.urls import path,include
from . import views


app_name = 'news_letter'
urlpatterns = [
    path('signup/', views.NewsletterSignupView.as_view(), name='newsletter_signup'),
]