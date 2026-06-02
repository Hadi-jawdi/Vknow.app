from django.urls import path
from .views import ScholarshipPageView, ScholarshipSearchAPIView


app_name = 'scholarship_app'

urlpatterns = [
    path('', ScholarshipPageView.as_view(), name='scholarships'),
    path('api/search/', ScholarshipSearchAPIView.as_view(), name='scholarship-search'),
]