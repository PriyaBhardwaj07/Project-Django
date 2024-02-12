from django.db import models
from authenticate.models import User
from productapp.models import Product
from cartapp.models import Cart
import random

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2, default =0)

    def save(self, *args, **kwargs):
        total = sum(item.products.price for item in self.cart.cart_items.all())
        self.Total_amount = total    
        super().save(*args, **kwargs)

rating_choices = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)
        
class FeedBack(models.Model):
    feedback = models.CharField(max_length = 500)
    user_id = models.ManyToManyField(User, related_name='feedback')
    rating_category = models.IntegerField(null = True, choices = rating_choices)
    product_id = models.ForeignKey(Product, related_name='feedback', on_delete=models.SET_NULL, null=True, blank=True)
   

