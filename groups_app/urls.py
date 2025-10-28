from django.urls import path
from . import views

app_name = "groups_app"

urlpatterns = [
    path("create/", views.create_group, name="create_group"),
    path("join/", views.join_group, name="join_group"),
    path("<int:group_id>/", views.group_detail, name="group_detail"),
]
