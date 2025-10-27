
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('account/', include("account_app.urls")),
    path('courses/', include("courses_app.urls")),
    path('discussion/', include("discussion_app.urls")),
    path('resources/', include("resources_app.urls")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)