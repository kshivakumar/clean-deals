from django.db import models
from django.core.validators import MinValueValidator


BASE_TAX_CREDIT_RATE = 0.3


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
            models.CheckConstraint(
                check=models.Q(transfer_rate__range=[0, 1]), name="transfer_rate_limits"
            ),
        ]

    @property
    def tax_credit_transfer_amount(self):
        return (
            self.project.fair_market_value * BASE_TAX_CREDIT_RATE * self.transfer_rate
        )
