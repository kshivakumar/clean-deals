from django.urls import path, include

from .views import ProjectView


urlpatterns = [
    path("projects/", ProjectView.as_view(), name="projects")
]
