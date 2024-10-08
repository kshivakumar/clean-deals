from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Deal, Project, ProjectDeal
from .serializers import (
    ProjectSerializer,
    DealListSerializer,
    DealCreateSerializer,
    DealDetailSerializer,
    ProjectDealCreateSerializer,
)


class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


class DealViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return DealListSerializer
        if self.action == "retrieve":
            return DealDetailSerializer
        if self.action == "create":
            return DealCreateSerializer
        raise NotImplementedError(f"action `{self.action}` not handled")

    def get_queryset(self):
        queryset = Deal.objects.all()
        if self.action == "retrieve":
            return queryset.prefetch_related("projects__project")
        return queryset

    def perform_create(self, serializer):
        with transaction.atomic():
            deal = serializer.save()
            projects = self.request.data.pop("projects", [])
            self._create_project_deals(deal.pk, projects)

    def _create_project_deals(self, deal_id, projects):
        for project in projects:
            deserializer = ProjectDealCreateSerializer(
                data={
                    "deal": deal_id,
                    "project": project["project"],
                    "transfer_rate": project["transfer_rate"],
                }
            )
            deserializer.is_valid(raise_exception=True)
            deserializer.save()


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def induct_project(request, deal_id):
    deserializer = ProjectDealCreateSerializer(
        data={
            "deal": deal_id,
            "project": request.data["project_id"],
            "transfer_rate": request.data["transfer_rate"],
        }
    )
    if deserializer.is_valid():
        deserializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"errors": [deserializer.errors]}
        )


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def withdraw_project(request, deal_id, project_id):
    pd = get_object_or_404(ProjectDeal, deal_id=deal_id, project_id=project_id)
    pd.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
