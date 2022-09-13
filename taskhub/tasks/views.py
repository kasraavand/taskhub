from urllib import request
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q as _Query
from tasks.models import Task
from tasks.permissions import UserIsOwnerTask
from tasks.serializers import taskserializer


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = taskserializer

    def get_queryset(self):
        if self.request.user.role == "manager":
            return Task.objects.filter(
                project_owner=self.request.user
                )
        else:
            # retriving tasks for the given user and other users in same project as the given user
            return Task.objects.filter(
                _Query(user=self.request.user) | _Query(project__developers=self.request.user)
                )

    def perform_create(self, serializer):
        if self.request.user.role == "manager":
            serializer.save()
        else:
            serializer.save(user=self.request.user)


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = taskserializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, UserIsOwnerTask)


