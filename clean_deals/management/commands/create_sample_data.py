import random

from django.core.management.base import BaseCommand
from django.db import transaction

from clean_deals.models import Project, Deal, ProjectDeal


class Command(BaseCommand):
    help = "Generates sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num_projects", type=int, default=50, help="No. of projects to create"
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            projects = self.gen_projects(options["num_projects"])
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
