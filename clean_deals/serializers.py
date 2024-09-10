from rest_framework import serializers

from clean_deals.models import Deal, Project, ProjectDeal


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "fair_market_value"]


class DealListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"
        read_only_fields = [f.name for f in Deal._meta.fields]


class DealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ["id", "name"]
        read_only_fields = ["id"]


class ProjectDealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDeal
        fields = ["project", "deal", "transfer_rate"]

    def validate_transfer_rate(self, value):
        if 0 <= value <= 1:
            return value
        raise serializers.ValidationError(
            f"value should be between 0 and 1, got {value}"
        )


class ProjectDealListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDeal
        fields = ["project", "tax_credit_transfer_amount"]


class DealDetailSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    total_tax_credit = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ["name", "projects", "total_tax_credit"]

    def get_projects(self, instance):
        return ProjectDealListSerializer(instance.projects, many=True).data

    def get_total_tax_credit(self, instance):
        return sum(p.tax_credit_transfer_amount for p in instance.projects.all())
