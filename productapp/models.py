from django.db import models
from django.utils.text import slugify

# Create your models here.

# class Product(models.Model):
#     name = models.CharField(max_length=50)
#     price = models.IntegerField(default=0) # we can set max or min value
#     description = models.CharField(max_length=50)
#     image = models.ImageField(upload_to='uploads/products/')
#     rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     discount = discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
#     colors = models.CharField(max_length=100, blank=True, null=True,default ='black')  # Allow multiple colors, so using CharField
#     STOCK_CHOICES = [
#         ('in_stock', 'In Stock'),
#         ('out_of_stock', 'Out of Stock'),
#     ]
class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='images/',null=True, blank=True) # how to upload and save them
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField()
    stock_status = models.CharField(max_length=12)
    color = models.CharField(max_length = 20)
    description = models.TextField(blank=True, max_length=500)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.stock_status = 'In Stock'
        else:
            self.stock_status = 'Out of Stock'

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
        
    
    
    
    
    
    
    
    
    
    
