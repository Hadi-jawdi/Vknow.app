from django.urls import path
from . import views

app_name = "discussion_app"

urlpatterns = [
    path("", views.discussion_list, name="list"),
    path("new/", views.discussion_post, name="new_post"),
    path("<int:post_id>/reply/", views.discussion_reply, name="reply"),
    path("<int:post_id>/reply/<int:parent_id>/", views.discussion_reply, name="reply_to_reply"),
]
