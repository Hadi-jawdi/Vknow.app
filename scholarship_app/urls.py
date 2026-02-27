from django.urls import path
from .views import ScholarshipPageView, ScholarshipSearchAPIView

urlpatterns = [
    path('', ScholarshipPageView.as_view(), name='scholarships'),
    path('api/search/', ScholarshipSearchAPIView.as_view(), name='scholarship-search'),
]