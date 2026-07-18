from django.urls import path

from . import views

app_name = "sat"

urlpatterns = [
    path("", views.start_test, name="start_test"),
    path("test/<uuid:attempt_id>/", views.take_test, name="take_test"),
    path("test/<uuid:attempt_id>/submit/", views.submit_test, name="submit_test"),
    path("test/<uuid:attempt_id>/results/", views.test_results, name="test_results"),
    path("history/", views.test_history, name="test_history"),
]
