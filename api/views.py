from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from campaigns.models import Campaign
from issues.models import Issue
from impact.services import get_impact_snapshot

from .serializers import CampaignSerializer, IssueSerializer, ImpactSnapshotSerializer


class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campaign.objects.filter(is_active=True).select_related("location")
    serializer_class = CampaignSerializer
    lookup_field = "slug"


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.select_related("category", "location").prefetch_related("timeline")
    serializer_class = IssueSerializer
    lookup_field = "slug"
    throttle_scope = "issue-create"

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class ImpactViewSet(viewsets.ViewSet):
    """Read-only impact endpoint — GET /api/v1/impact/snapshot/?city=Jaipur"""

    def list(self, request):
        city = request.query_params.get("city", "")
        snapshot = get_impact_snapshot(city)
        return Response(ImpactSnapshotSerializer(snapshot).data)
