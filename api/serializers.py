from rest_framework import serializers

from campaigns.models import Campaign
from issues.models import Issue, IssueUpdate
from impact.models import ImpactSnapshot


class CampaignSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    progress_percent = serializers.ReadOnlyField()
    volunteer_count = serializers.ReadOnlyField()

    class Meta:
        model = Campaign
        fields = [
            "id", "title", "slug", "campaign_type", "objective", "location",
            "start_date", "end_date", "goal_count", "progress_count",
            "progress_percent", "volunteer_count", "is_active",
        ]


class IssueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueUpdate
        fields = ["status", "note", "created_at"]


class IssueSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    timeline = IssueUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id", "title", "slug", "category", "description", "location",
            "severity", "is_recurring", "status", "supporter_count",
            "created_at", "timeline",
        ]
        read_only_fields = ["status", "supporter_count", "slug"]

    def create(self, validated_data):
        validated_data["reporter"] = self.context["request"].user
        return super().create(validated_data)


class ImpactSnapshotSerializer(serializers.ModelSerializer):
    survival_rate_percent = serializers.ReadOnlyField()
    resolution_rate_percent = serializers.ReadOnlyField()

    class Meta:
        model = ImpactSnapshot
        fields = "__all__"
