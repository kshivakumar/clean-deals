import random

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from clean_deals.models import Project, Deal, ProjectDeal


NUM_PROJECTS = 50


class Command(BaseCommand):
    help = "Generates sample data and test user, should be executed only once"

    def handle(self, *args, **options):
        self.create_test_user()
        self.gen_sample_data()

    def gen_sample_data(self):
        with transaction.atomic():
            projects = self.gen_projects(NUM_PROJECTS)
            self.gen_deals_and_project_deals(projects)
        self.stdout.write(
            f"Successfully generated sample data for {len(projects)} projects!"
        )

    def gen_projects(self, num_projects):
        projects = []
        for i in range(num_projects):
            project = Project.objects.create(
                name=f"Project {i+1}",
                fair_market_value=random.randrange(10_000, 1_005_000, 5_000),
            )
            projects.append(project)
        return projects

    def gen_deals_and_project_deals(self, projects):
        num_deals = 3 * len(projects)
        for i in range(num_deals):
            deal = Deal.objects.create(name=f"Deal {i+1}")
            num_projects_to_link = random.randint(1, min(len(projects), 5))
            for project in random.sample(projects, num_projects_to_link):
                ProjectDeal.objects.create(
                    project=project, deal=deal, transfer_rate=random.uniform(0, 1)
                )

    def create_test_user(self):
        username = password = "test"
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password,
            email="hello@example.com",
        )
        self.stdout.write(
            f"Successfully created a test user with credentials, username: {username}, password: {password}, token: {user.auth_token.key}"
        )
