from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    AVAILABILITY_CHOICES = [
        ("weekday", "Weekdays"),
        ("weekend", "Weekends"),
        ("evening", "Evenings"),
        ("flexible", "Flexible"),
    ]
    AGE_GROUP_CHOICES = [
        ("under_18", "Under 18"),
        ("18_24", "18–24"),
        ("25_40", "25–40"),
        ("41_60", "41–60"),
        ("60_plus", "60+"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_profile")
    mobile = models.CharField(max_length=20)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="volunteers")
    interests = models.CharField(max_length=255, blank=True)
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default="flexible")
    emergency_contact = models.CharField(max_length=100, blank=True)
    consent_given = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Volunteer: {self.user}"
