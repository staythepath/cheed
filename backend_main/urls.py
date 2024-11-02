from django.contrib import admin
from django.urls import path, include
from backend_main import views
from activitypub_server.views import webfinger  # Import webfinger directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activitypub/', include('activitypub_server.urls')),
    path('', views.home, name='home'),  # Root URL route
    path('.well-known/webfinger', webfinger, name='webfinger'),  # Ensure WebFinger is at the root
]
