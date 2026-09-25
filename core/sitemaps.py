from django.contrib.sitemaps import Sitemap

from campaigns.models import Campaign
from issues.models import Issue
from events.models import Event
from content.models import BlogPost


class CampaignSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Campaign.objects.filter(is_active=True)


class IssueSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Issue.objects.all()


class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Event.objects.all()


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(is_published=True)


sitemaps = {
    "campaigns": CampaignSitemap,
    "issues": IssueSitemap,
    "events": EventSitemap,
    "blog": BlogSitemap,
}
