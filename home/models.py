from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
