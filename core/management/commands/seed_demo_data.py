import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Location, Category
from campaigns.models import Campaign
from issues.models import Issue
from events.models import Event


class Command(BaseCommand):
    help = "Seeds a small set of demo records so the site isn't empty on first run."

    def handle(self, *args, **options):
        if Campaign.objects.exists():
            self.stdout.write(self.style.WARNING("Demo data already present — skipping."))
            return

        team_user, _ = User.objects.get_or_create(
            username="envirgreen_team", defaults={"email": "team@envirgreen.org"}
        )
        team_user.profile.role = "envirgreen_team"
        team_user.profile.city = "Jaipur"
        team_user.profile.save()

        loc_ward12 = Location.objects.create(city="Jaipur", area="Ward 12")
        loc_sector9 = Location.objects.create(city="Jaipur", area="Sector 9")

        cat_garbage, _ = Category.objects.get_or_create(
            name="Garbage dumping", slug="garbage-dumping", category_type="issue"
        )
        Category.objects.get_or_create(name="Civic Sense", slug="civic-sense", category_type="blog")

        campaign = Campaign.objects.create(
            title="Clean Streets, Ward 12",
            campaign_type="street_cleanup",
            objective=(
                "Clear and prevent re-accumulation of garbage dumping points along the "
                "Ward 12 main road, through three coordinated weekend cleanup drives."
            ),
            location=loc_ward12,
            start_date=datetime.date.today(),
            organizer=team_user,
            goal_count=3,
            progress_count=1,
        )

        Issue.objects.create(
            title="Overflowing garbage bin — Sector 9 Market Road",
            category=cat_garbage,
            reporter=team_user,
            description=(
                "The public bin near the Sector 9 market entrance has been overflowing "
                "for several days, with waste spreading onto the footpath."
            ),
            location=loc_sector9,
            severity="medium",
            is_recurring=True,
            status="reported_to_authority",
        )

        Event.objects.create(
            title="Ward 12 Sunday Cleanup Drive #1",
            campaign=campaign,
            location=loc_ward12,
            start_time=timezone.now() + datetime.timedelta(days=3),
            organizer=team_user,
            capacity=20,
        )

        self.stdout.write(self.style.SUCCESS("Seeded 1 campaign, 1 issue, 1 event."))
