# Generated by Django 4.2.9 on 2024-02-06 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appvincartapp', '0002_category_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appvincartapp.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]