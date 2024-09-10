from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from clean_deals.models import Project, Deal, ProjectDeal


class TestProjectView(APITestCase):

    def test_create_project(self):
        response = self.client.post(
            reverse("projects"),
            data={"name": "Take-home project", "fair_market_value": 250000},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, "Take-home project")

    def test_list_projects(self):
        Project.objects.create(name="P1", fair_market_value=1000)
        Project.objects.create(name="P2", fair_market_value=2000)

        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TestDealView(APITestCase):
    pass


class TestProjectInduction(APITestCase):

    def test_induct_existing_project(self):
        pass

    def test_induct_project_invalid_transfer_rate(self):
        pass
