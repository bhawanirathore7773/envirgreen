from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Extends Django's built-in User with Envirgreen-specific fields.

    Verification tiers (see docs/02-core-platform-systems.md, Verification
    System): badges must be meaningful and are set by the team, never
    purchasable or self-assigned.
    """

    ROLE_CHOICES = [
        ("community_member", "Community Member"),
        ("verified_volunteer", "Verified Volunteer"),
        ("campaign_volunteer", "Campaign Volunteer"),
        ("envirgreen_team", "Envirgreen Team"),
        ("partner_org", "Partner Organisation"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="community_member")
    city = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=280, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-joined_at"]

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"username": self.user.username})

    # --- Impact stats -----------------------------------------------------
    # Computed from real records, never hand-edited, per the platform's
    # anti-fake-impact rule (docs/02-core-platform-systems.md, Impact system).

    @property
    def trees_planted(self):
        return self.user.tree_plantations.filter(status__in=["verified", "growing", "survived"]).aggregate(
            models.Sum("count")
        )["count__sum"] or 0

    @property
    def issues_reported(self):
        return self.user.reported_issues.count()

    @property
    def campaigns_joined(self):
        return self.user.campaign_memberships.count()

    @property
    def badges_count(self):
        return self.user.badges.count()

    @property
    def action_score(self):
        """A simple, transparent starting formula for the Envirgreen Action
        Score. Weighting is intentionally documented and editable in one
        place — see docs/02-core-platform-systems.md, Gamification."""
        return (
            self.trees_planted * 2
            + self.issues_reported * 3
            + self.campaigns_joined * 5
            + self.badges_count * 4
        )
