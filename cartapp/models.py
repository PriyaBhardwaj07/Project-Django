from django.db import models
from authenticate.models import User
from productapp.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "carts", null=True)
    is_paid = models.BooleanField(default=False)
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = "cart_items")
    products = models.ForeignKey(Product, on_delete=models.SET_NULL,null =True, blank = True)
    quantity = models.PositiveIntegerField(default = 1)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.products:
            if self.products.stock_status == 'IN_STOCK':
                if self.products.quantity >= self.quantity:
                    self.products.quantity -= self.quantity
                    self.products.save()


                    
class SaveForLater(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    products_id = models.ManyToManyField(Product)

