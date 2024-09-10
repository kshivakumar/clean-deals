from rest_framework import generics

from .models import Deal, Project, ProjectDeal
from .serializers import ProjectSerializer


class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
