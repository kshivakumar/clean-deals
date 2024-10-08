from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


BASE_TAX_CREDIT_RATE = 0.3


class User(AbstractUser):
    pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Project(models.Model):
    name = models.CharField(max_length=100)
    fair_market_value = models.FloatField(
        validators=[MinValueValidator(0)], help_text="In USD"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(fair_market_value__gt=0), name="positive_fmv"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.pk})"


class Deal(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class ProjectDeal(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="projects")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="deals")
    transfer_rate = models.FloatField(help_text="Tax Credit Transfer Rate")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["deal", "project"], name="unique_deal_project"
            ),
            models.CheckConstraint(
                check=models.Q(transfer_rate__range=[0, 1]), name="transfer_rate_limits"
            ),
        ]

    def __str__(self):
        return f"{str(self.project)} / {str(self.deal)}"

    @property
    def tax_credit_transfer_amount(self):
        return (
            self.project.fair_market_value * BASE_TAX_CREDIT_RATE * self.transfer_rate
        )
