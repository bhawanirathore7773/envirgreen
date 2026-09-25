from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import Location
from campaigns.models import Campaign


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    campaign = models.ForeignKey(Campaign, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    meeting_point = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    required_equipment = models.CharField(max_length=255, blank=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:180]
            slug = base
            i = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug": self.slug})

    @property
    def registered_count(self):
        return self.registrations.count()

    @property
    def spots_left(self):
        if self.capacity is None:
            return None
        return max(0, self.capacity - self.registered_count)


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    attended = models.BooleanField(default=False, help_text="Set by the organizer after the event — this, not the registration itself, counts toward impact.")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user} @ {self.event}"
