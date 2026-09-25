from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from core.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("campaigns/", include("campaigns.urls")),
    path("events/", include("events.urls")),
    path("volunteer/", include("volunteers.urls")),
    path("issues/", include("issues.urls")),
    path("trees/", include("trees.urls")),
    path("community/", include("community.urls")),
    path("donate/", include("donations.urls")),
    path("impact/", include("impact.urls")),
    path("notifications/", include("notifications.urls")),
    path("blog/", include("content.urls")),
    path("api/v1/", include("api.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
