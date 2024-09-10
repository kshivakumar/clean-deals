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

