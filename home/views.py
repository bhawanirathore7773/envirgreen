from django.shortcuts import render
from .models import Product

def homepage_view(request):
    # Fetch "Best Deals" products
    best_deals = Product.objects.filter(is_best_deal=True).order_by('-rating')[:6]  # Limit to top 10 products

    # Render the homepage template
    return render(request, 'home/index.html', {
        'best_deals': best_deals,
    })
