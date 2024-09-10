from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectView, DealViewSet, induct_project, withdraw_project

router = DefaultRouter()
router.register("deals", DealViewSet, basename="deals")

urlpatterns = [
    path("", include(router.urls)),
    path("projects/", ProjectView.as_view(), name="projects"),
    path("deals/<int:deal_id>/projects/", induct_project, name="induct-project"),
    path(
        "deals/<int:deal_id>/projects/<int:project_id>/",
        withdraw_project,
        name="withdraw-project",
    ),
]
