from django.db import models


class Location(models.Model):
    """Shared geography reference used by issues, campaigns, trees, and events."""

    city = models.CharField(max_length=100)
    area = models.CharField("Area / ward", max_length=150, blank=True)
    address_line = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    show_approximate_only = models.BooleanField(
        default=True,
        help_text="If true, only city/area is shown publicly — exact coordinates are hidden.",
    )

    class Meta:
        ordering = ["city", "area"]

    def __str__(self):
        return f"{self.area + ', ' if self.area else ''}{self.city}"


class Category(models.Model):
    """Shared tag/category model used by issues and blog content."""

    CATEGORY_TYPES = [
        ("issue", "Environmental Issue"),
        ("blog", "Blog / Content"),
        ("campaign", "Campaign"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["category_type", "name"]

    def __str__(self):
        return self.name
