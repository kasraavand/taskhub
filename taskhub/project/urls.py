from django.urls import path
from .views import ProjectListCreateAPIView, ProjectDetailAPIView

app_name = 'project'

urlpatterns = [
    path('', ProjectListCreateAPIView.as_view(), name="projects"),
    path('<str:pk>/', ProjectDetailAPIView.as_view(), name="project_detail")
]
