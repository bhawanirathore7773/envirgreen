from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CampaignViewSet, IssueViewSet, ImpactViewSet

router = DefaultRouter()
router.register("campaigns", CampaignViewSet, basename="api-campaigns")
router.register("issues", IssueViewSet, basename="api-issues")
router.register("impact/snapshot", ImpactViewSet, basename="api-impact")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
