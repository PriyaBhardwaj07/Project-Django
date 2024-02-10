from django.db import models
from authenticate.models import User
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='images/',null=True, blank=True) # how to upload and save them
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField(default=0)
    #quantity = models.IntegerField()
    stock_status = models.CharField(default='OUT-OF-STOCK', max_length=12)
    #color = models.CharField(max_length = 20)
    color = models.CharField(max_length=50, default='')
    description = models.TextField(blank=True, max_length=500)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.stock_status = 'IN-STOCK'
        else:
            self.stock_status = 'OUT-OF-STOCK'

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
        
    
    
    
    
    
    
    
    
    
    
