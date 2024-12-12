from home.models import Category

categories = [
    {"name": "Electronics", "description": "Explore a wide range of gadgets like smartphones, laptops, and smartwatches.", "image_name": "electronics.jpg"},
    {"name": "Fashion", "description": "Find trendy clothing, footwear, and accessories for men, women, and kids.", "image_name": "fashion.jpg"},
    {"name": "Home Appliances", "description": "Upgrade your home with modern kitchen and home appliances.", "image_name": "home_appliances.jpg"},
    {"name": "Beauty & Personal Care", "description": "Discover skincare, makeup, and grooming essentials for all.", "image_name": "beauty_personal.jpg"},
    {"name": "Groceries", "description": "Get fresh fruits, vegetables, and daily essentials delivered to your doorstep.", "image_name": "groceries.jpg"},
    {"name": "Health & Wellness", "description": "Shop for fitness equipment, supplements, and wellness products.", "image_name": "health_wellness.jpg"},
    {"name": "Toys & Games", "description": "Find fun and educational toys and games for kids of all ages.", "image_name": "toys_games.jpg"},
    {"name": "Sports & Outdoors", "description": "Gear up with sports equipment and outdoor adventure essentials.", "image_name": "sports_outdoors.jpg"},
    {"name": "Books & Stationery", "description": "Discover a wide selection of books and office supplies.", "image_name": "books_stationery.jpg"},
    {"name": "Furniture", "description": "Elegant furniture for your living room, bedroom, and office spaces.", "image_name": "furniture.jpg"},
    {"name": "Automotive", "description": "Accessories and tools for your car or bike needs.", "image_name": "automotive.jpg"},
    {"name": "Baby Products", "description": "Baby essentials, toys, and clothing for newborns and toddlers.", "image_name": "baby_products.jpg"},
    {"name": "Pet Supplies", "description": "Food, toys, and care products for your furry friends.", "image_name": "pet_supplies.jpg"},
    {"name": "Jewelry", "description": "Stunning collections of rings, necklaces, and bracelets.", "image_name": "jewelry.jpg"},
    {"name": "Watches", "description": "Premium and stylish watches for every occasion.", "image_name": "watches.jpg"},
    {"name": "Bags & Luggage", "description": "Find backpacks, handbags, and travel luggage for all your needs.", "image_name": "bags_luggage.jpg"},
    {"name": "Kitchenware", "description": "Cook and dine in style with our collection of kitchen essentials.", "image_name": "kitchenware.jpg"},
    {"name": "Home Décor", "description": "Beautiful decorations to enhance your living spaces.", "image_name": "home_decor.jpg"},
    {"name": "Mobile Accessories", "description": "Cases, chargers, and gadgets to complement your smartphone.", "image_name": "mobile_accessories.jpg"},
    {"name": "Footwear", "description": "Comfortable and stylish shoes for every occasion.", "image_name": "footwear.jpg"}
]

for category in categories:
    Category.objects.create(**category)

print("Categories added successfully!")
