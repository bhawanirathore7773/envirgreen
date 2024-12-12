from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True)
    discount = models.PositiveIntegerField(default=0)  # Discount in percentage
    rating = models.FloatField(default=0.0)  # Product rating out of 5
    delivery_date = models.DateField(default=now)  # Estimated delivery date
    image = models.ImageField(upload_to='products/')  # Product image
    is_best_deal = models.BooleanField(default=False)  # Mark as best deal

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def final_price(self):
        """
        Calculate the price after the discount.
        """
        return self.price - (self.price * self.discount / 100)

    def __str__(self):
        return self.name
