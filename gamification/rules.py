"""Badge-awarding rules, decoupled from the models that trigger them.

Wired up via signal receivers in gamification/signals.py. Never award a
badge from user-editable input — only from verified-status changes on
Issue, TreePlantation, or EventRegistration records.
"""

from .models import Badge, UserBadge


def award_badge(user, slug):
    badge = Badge.objects.filter(slug=slug).first()
    if badge:
        UserBadge.objects.get_or_create(user=user, badge=badge)


def check_first_tree(user):
    if user.tree_plantations.filter(status__in=["verified", "growing", "survived"]).exists():
        award_badge(user, "first-tree")


def check_clean_start(user):
    from campaigns.models import CampaignMember

    if CampaignMember.objects.filter(user=user, support_type="volunteer").exists():
        award_badge(user, "clean-start")
