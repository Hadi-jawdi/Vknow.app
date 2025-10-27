from django.urls import path
from . import views

app_name = "resources_app"

urlpatterns = [
    
    
# New resource routes
    path("", views.resource_list, name="resources"),
    path("share/", views.share_resource, name="share_resource"),
    path("resources/<int:pk>/", views.resource_detail, name="resource_detail"),
    

]
