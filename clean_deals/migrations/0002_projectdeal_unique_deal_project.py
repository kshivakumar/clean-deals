# Generated by Django 4.2.15 on 2024-09-10 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clean_deals", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="projectdeal",
            constraint=models.UniqueConstraint(
                fields=("deal", "project"), name="unique_deal_project"
            ),
        ),
    ]
