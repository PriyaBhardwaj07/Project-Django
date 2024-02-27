
# #  ======= CORRECT ========

# # from django.db import models
# # from authenticate.models import User

# # class StripeCustomer(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     stripe_customer_id = models.CharField(max_length=255)
   
# #     def __str__(self):
# #         return f"{self.user.username}'s Stripe Customer"

# # class PaymentMethod(models.Model):
# #     customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)
# #     stripe_payment_method_id = models.CharField(max_length=255)
# #     # MORE FIELDS CAN BE ADDED 

# #     def __str__(self):
# #         return f"Payment Method {self.id} of {self.customer.user.username}"


# # ================CORRECT============

# # ----- FOR PAYMENT INTENT -----------------
# # from django.db import models
# # from django.conf import settings
# # from authenticate.models import User
# # import stripe

# # stripe.api_key = settings.STRIPE_SECRET_KEY

# # class StripeCustomer(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     stripe_customer_id = models.CharField(max_length=255)

# #     def __str__(self):
# #         return f"{self.user.username}'s Stripe Customer"

# # class PaymentMethod(models.Model):
# #     customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)
# #     stripe_payment_method_id = models.CharField(max_length=255)
# #     # Add any other fields related to your payment method here

# #     def __str__(self):
# #         return f"Payment Method {self.id} of {self.customer.user.username}"

# #     def create_payment_intent(self, amount):
# #         try:
# #             payment_intent = stripe.PaymentIntent.create(
# #                 amount=amount,
# #                 currency='usd',
# #                 customer=self.customer.stripe_customer_id,
# #                 payment_method=self.stripe_payment_method_id,
# #                 confirmation_method='manual',
# #                 confirm=True,
# #             )
# #             return payment_intent.client_secret
# #         except stripe.error.StripeError as e:
# #             # Handle Stripe errors here
# #             return None


# from django.db import models
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from authenticate.models import User

# # Create your models here.
# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_paid = models.BooleanField(default=False) #to determine if payment is done making or not
#     client_secret = models.CharField(max_length=255)
#     amount_paid = models.FloatField()

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from authenticate.models import User

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False) 
    client_secret = models.CharField(max_length=255)
    amount_paid = models.FloatField()
