from django.db import models

class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    firstName = models.CharField(max_length = 50)
    lastName =  models.CharField(max_length = 50)
    email = models.EmailField()
    phone = models.CharField(max_length = 50)
    address = models.TextField()
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    password = models.CharField(max_length=1000,blank=True, null=True)
    
    def register(self):
        self.save()
        
    
    
    