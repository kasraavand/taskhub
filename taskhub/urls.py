from django.urls import include, path
from django.contrib import admin


api_urls = [
    path('projects/', include('project.urls')),
    path('tasks/', include('tasks.urls')),
    path('', include('users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
