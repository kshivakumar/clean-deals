from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from clean_deals.models import Project, Deal, ProjectDeal
from clean_deals.views import DealViewSet


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

    def test_create_deal_with_projects(self):
        p1 = Project.objects.create(name="P1", fair_market_value=750)
        p2 = Project.objects.create(name="P2", fair_market_value=250)
        data = {
            "name": "Bow-bow",
            "projects": [
                {"project": p1.id, "transfer_rate": 0.9},
                {"project": p2.id, "transfer_rate": 0.8},
            ],
        }

        response = self.client.post(reverse("deals-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Deal.objects.count(), 1)
        self.assertEqual(ProjectDeal.objects.count(), 2)

    def test_list_deals(self):
        Deal.objects.create(name="D1")
        Deal.objects.create(name="D2")
        Deal.objects.create(name="D3")

        response = self.client.get(reverse("deals-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_deal_with_tax_credit_calculation(self):
        deal = Deal.objects.create(name="SuperDeal")
        p1 = Project.objects.create(name="P1", fair_market_value=1234)
        p2 = Project.objects.create(name="P2", fair_market_value=1234)
        ProjectDeal.objects.create(deal=deal, project=p1, transfer_rate=0.25)
        ProjectDeal.objects.create(deal=deal, project=p2, transfer_rate=0.75)

        url = reverse("deals-detail", kwargs={"pk": deal.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "SuperDeal")
        self.assertEqual(len(response.data["projects"]), 2)
        self.assertEqual(
            response.data["total_tax_credit"], (1234 * 0.3 * 0.25) + (1234 * 0.3 * 0.75)
        )

    def test_unhandled_action_raises_not_implemented_error(self):
        view = DealViewSet()
        view.action = "destroy"
        with self.assertRaises(NotImplementedError) as ctx:
            view.get_serializer_class()
        self.assertEqual("action `destroy` not handled", str(ctx.exception))


class TestProjectInduction(APITestCase):

    def test_induct_project(self):
        deal = Deal.objects.create(name="Deal555")
        project = Project.objects.create(name="Project666", fair_market_value=50_000)

        response = self.client.post(
            reverse("induct-project", kwargs={"deal_id": deal.id}),
            data={"project_id": project.id, "transfer_rate": 0.25},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectDeal.objects.count(), 1)
        pd = ProjectDeal.objects.first()
        self.assertEqual(pd.deal, deal)
        self.assertEqual(pd.project, project)
        self.assertEqual(pd.transfer_rate, 0.25)

    def test_induct_existing_project(self):
        deal = Deal.objects.create(name="Deal555")
        project = Project.objects.create(name="Project666", fair_market_value=50_000)

        self.client.post(
            reverse("induct-project", kwargs={"deal_id": deal.id}),
            data={"project_id": project.id, "transfer_rate": 0.25},
        )
        response = self.client.post(
            reverse("induct-project", kwargs={"deal_id": deal.id}),
            data={"project_id": project.id, "transfer_rate": 0.25},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProjectDeal.objects.count(), 1)
        self.assertEqual(
            response.data["errors"][0]["non_field_errors"][0].code, "unique"
        )

    def test_induct_project_invalid_transfer_rate(self):
        deal = Deal.objects.create(name="Extreme Deal")
        project = Project.objects.create(name="Bad Project", fair_market_value=91919191)

        response = self.client.post(
            reverse("induct-project", kwargs={"deal_id": deal.id}),
            data={"project_id": project.id, "transfer_rate": 55.55},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProjectDeal.objects.count(), 0)


class TestProjectWithdrawal(APITestCase):

    def test_withdraw_project(self):
        deal = Deal.objects.create(name="Chota Deal")
        project = Project.objects.create(name="Bada Project", fair_market_value=50)
        ProjectDeal.objects.create(deal=deal, project=project, transfer_rate=0.75)

        url = reverse(
            "withdraw-project", kwargs={"deal_id": deal.id, "project_id": project.id}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_withdraw_nonexisting_project(self):
        deal = Deal.objects.create(name="No Deal")

        url = reverse(
            "withdraw-project", kwargs={"deal_id": deal.id, "project_id": 999}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
