from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .permissions import UserIsManager, UserIsProjectOwner
from .serializers import ProjectSerializer




class ProjectListCreateAPIView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, UserIsManager)

    def get_queryset(self):
        if self.request.user.role == "manager":
            return Project.objects.filter(manager=self.request.user)
        else:
            return Project.objects.filter(developers=self.request.user)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated, UserIsProjectOwner)


