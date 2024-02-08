from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0) # we can set max or min value
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/products/')
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount = discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    colors = models.CharField(max_length=100, blank=True, null=True,default ='black')  # Allow multiple colors, so using CharField
    STOCK_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    Stock = models.CharField(max_length=20, choices=STOCK_CHOICES, default='in_stock')
    # to fetch all products
    @staticmethod 
    def get_all():
        return Product.objects.all() 
    @staticmethod
    def get_all_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all()
        

    
    
    
    