# home/migrations/000X_add_category_to_product.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('home', 'previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(to='home.Category', on_delete=models.CASCADE),
        ),
    ]
