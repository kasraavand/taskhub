from django.urls import path
from tasks.views import TaskListCreateAPIView, TaskDetailAPIView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListCreateAPIView.as_view(), name="list"),
    path('<int:pk>/', TaskDetailAPIView.as_view(), name="detail"),
]
