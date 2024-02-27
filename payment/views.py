import time
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.views import View
import stripe
from django.views.decorators.csrf import csrf_exempt
from authenticate.models import User
from orderapp.models import Order
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request,*args,**kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        order_ids = request.GET.getlist('order_ids[]') 
        orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
        total_amount = 0
        for order_id in order_ids:
            order = Order.objects.get(pk=order_id)
            products = order.product.all()
            order_amount = sum(product.price for product in products)
            total_amount += order_amount
        context = {
                'user': user,
                'orders': orders,
                'total_amount': total_amount,
            }
        request.session['order_ids'] = order_ids
        return render(request, 'proceed_payment.html',context)

    def post(self, request,*args,**kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        order_ids = request.session.get('order_ids', [])
        payment_method_id = request.POST.get('paymentMethodId')
        currency = 'usd'
        shipping_name = request.POST.get('shippingName')  # Retrieve shipping name from request
        shipping_address = request.POST.get('shippingAddress')
        shipping_city = request.POST.get('shippingCity')
        shipping_country = request.POST.get('shippingCountry')
        shipping_state = request.POST.get('shippingState')

        try:
            total_amount = 0 
            payment_intent_items = []

            for order_id in order_ids:
                order = Order.objects.get(pk=order_id)
                products = order.product.all()  
                order_amount = sum(product.price for product in products)
                total_amount += order_amount  
                for product in products:
                    payment_intent_items.append({
                        'amount': product.price * 100,
                        'currency': currency,
                        'description': product.name,
                        'quantity': 1, 
                    })
            print(payment_intent_items)
            customer = stripe.Customer.create(
                name=user.first_name,
                email=user.email,
            )
            
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer.id
            )
            
            stripe.PaymentMethod.modify(
                payment_method_id,
                billing_details={
                    'name': shipping_name,
                    'address': {
                        'line1': shipping_address,
                        "city": shipping_city,
                        "country": shipping_country,
                        "state": shipping_state
                    }
                }
            )
            
            payment_intent = stripe.PaymentIntent.create(
                amount=int(float(total_amount) * 100),
                currency=currency,
                customer=customer.id,
                payment_method=payment_method_id,
                # description=f"Payment for multiple orders: {payment_method_id}",
                description=f"Payment ID : {payment_method_id}",

                metadata={'order_ids': str(order_ids)},
            )

            payment = Payment.objects.create(user=user,amount_paid=total_amount, client_secret=payment_intent.client_secret)
            payment.save()
            client_secret = payment_intent.client_secret
            request.session['order_ids'] = order_ids
            request.session['client_secret'] = payment_intent.client_secret
            request.session['payment_id']= payment.id
            return redirect('pay_for_checkout', user_id=user_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class PayForCheckoutView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,*args,**kwargs):
        client_secret = request.session.get('client_secret','')
        payment_id = request.session.get('payment_id',0)
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
        order_ids = request.session.get('order_ids', [])
        orders = Order.objects.filter(id__in=order_ids)
        print(orders)
        print(client_secret)
        total_amount = 0
        for order_id in order_ids:
                order = Order.objects.get(pk=order_id)
                products = order.product.all()
                order_amount = sum(product.price for product in products)
                total_amount += order_amount
        context = {
            'client_secret': client_secret,
            'user': user,
            'orders': orders,
            'total_amount': total_amount,
            'payment_id': payment_id
        }
        return render(request, 'pay.html',context) 

class PaymentSuccessView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get('payment_id')
        payment = get_object_or_404(Payment, pk=payment_id)
        payment.is_paid = True
        payment.save()
        return render(request, 'success.html')



class PaymentRefundView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        client_secret = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(user=user_id, client_secret=client_secret)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)
        try:
            id = client_secret.split('_')[1]
            payment_intent_id='pi_'+id
            print(payment_intent_id)
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=int(payment.amount_paid),
            )
            return JsonResponse({'message': 'Refund successful'}, status=200)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class PaymentListView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        payments = Payment.objects.filter(user=user, is_paid=True)
        return render(request, 'display.html', {'payments': payments})
























# from django.shortcuts import render
# from django.http import JsonResponse
# import stripe
# from django.core.mail import send_mail
# import payment

# # Assuming you've already configured your Stripe API keys
# stripe.api_key = 'your_stripe_secret_key'

# def add_payment_method(request):
#     if request.method == 'POST':
#         payment_method_id = request.POST.get('payment_method_id')
        
#         try:
#             # Create a new customer in Stripe
#             customer = stripe.Customer.create(
#                 payment_method=payment_method_id,
#                 email=request.user.email,  # Assuming you have a user object
#                 invoice_settings={
#                     'default_payment_method': payment_method_id
#                 }
#             )
            
            # Optionally, save the payment method ID to your user's profile
            # request.user.payment_method_id = payment_method_id
            # request.user.save()

#             # Render payment.html template with success message
#             return render(request, 'payment.html', {'success': True})
#         except stripe.error.InvalidRequestError as e:
#             # Return error response if the payment method ID is invalid
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             # Return error response for other exceptions
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         # Render the payment_form.html template for GET requests
#         return render(request, 'payment.html')
       
# def process_payment(request):
#     if request.method == 'POST':
#         payment_method_id = request.POST.get('payment_method_id')

#         try:
#             # Confirm the payment with Stripe
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=1000,  # Adjust amount as needed (in cents)
#                 currency='usd',
#                 payment_method=payment_method_id,
#                 confirmation_method='manual',
#                 confirm=True,
#             )

#             # Log the payment intent ID to the console for debugging
#             print('Payment Intent ID:', payment_intent.id)

#             # Save payment information to database (optional)
#             payment.objects.create(payment_method_id=payment_method_id, user=request.user)

#             # Send email notification
#             send_mail(
#                 'Payment Successful',
#                 'Your payment was successful.',
#                 'bhardwajpriya2002@gmail.com',  # sender email
#                 ['bhardwajpriya2002@gmail.com'],  #  recipient email
#                 fail_silently=False,
#             )

#             # Render payment confirmation template with payment intent
#             return render(request, 'success.html', {'payment_intent': payment_intent})
#         except stripe.error.StripeError as e:
#             # Log the error to the console for debugging
#             print('Stripe Error:', str(e))

#             return render(request, 'failure.html', {'error': str(e), 'payment_intent': None})
#     else:
#         # Return error response if request method is not POST
#         return render(request, 'success.html', {'payment_intent': None})


# from django.shortcuts import render
# from django.http import JsonResponse
# import stripe
# from django.core.mail import send_mail
# from .models import PaymentIntent

# # Assuming you've already configured your Stripe API keys
# stripe.api_key = 'your_stripe_secret_key'

# def process_payment(request):
#     if request.method == 'POST':
#         payment_method_id = request.POST.get('payment_method_id')

#         try:
#             # Confirm the payment with Stripe
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=1000,  # Adjust amount as needed (in cents)
#                 currency='usd',
#                 payment_method=payment_method_id,
#                 confirmation_method='manual',
#                 confirm=True,
#             )

#             # Log the payment intent ID to the console for debugging
#             print('Payment Intent ID:', payment_intent.id)

#             # Save payment information to the database
#             PaymentIntent.objects.create(
#                 customer=request.user.stripecustomer,  # Assuming you have a StripeCustomer associated with the user
#                 payment_intent_id=payment_intent.id,
#                 amount=payment_intent.amount,
#                 currency=payment_intent.currency,
#                 status=payment_intent.status,
#             )


#             # Render payment confirmation template with payment intent
#             return render(request, 'success.html', {'payment_intent': payment_intent})
#         except stripe.error.StripeError as e:
#             # Log the error to the console for debugging
#             print('Stripe Error:', str(e))

#             return render(request, 'failure.html', {'error': str(e), 'payment_intent': None})
#     else:
#         # Return error response if the request method is not POST
#         return render(request, 'success.html', {'payment_intent': None})

# ========================= CORRECT CODE =====================================

# from django.shortcuts import render
# from django.http import JsonResponse
# import stripe

# stripe.api_key = 'sk_test_51OkIzmSGCDrMJpDVDDm6L0HgAtHdB2VNSB9MymLtDJhrQM28GSInbhT3Vqw1DsdZd6cgbK19ZGTNWz7Im5OCZGxM00uj1QQ0O9'

# def add_payment_method(request):
#     if request.method == 'POST':
#         payment_method_id = request.POST.get('payment_method_id')
        
#         try:
#             # Create a new customer in Stripe
#             customer = stripe.Customer.create(
#             payment_method=payment_method_id,
#             email=request.user.email,  
#             invoice_settings={
#                     'default_payment_method': payment_method_id
#                 }
#             )
            
#             # Optionally, save the payment method ID to your user's profile
#             # CHECK THESE 2 LINES 
#             request.user.payment_method_id = payment_method_id
#             request.user.save()
            
#             return render(request, 'payment.html', {'success': True})
#         except stripe.error.InvalidRequestError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return render(request, 'payment.html')

# def process_payment(request):
#     if request.method == 'POST':
#         payment_method_id = request.POST.get('payment_method_id')
#         try:
#             payment_intent = stripe.PaymentIntent.create( # for stripe payment 
#                 amount=2000,
#                 currency="usd",
#                 automatic_payment_methods={"enabled": True},
#                 payment_method_types=["card"],
# )
#             return render(request, 'success.html', {'payment_intent': payment_intent})
#         except stripe.error.StripeError as e:
#             return render(request, 'failure.html', {'error': str(e), 'payment_intent': None})

#     else:
#       payment_intent = stripe.PaymentIntent.create(
              
#                 amount=2000,
#                 currency="usd",
#                 automatic_payment_methods={"enabled": True},)
               
#       return render(request, 'success.html', {'payment_intent': payment_intent})
  

# ========================= CORRECT CODE =====================================

# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views import View
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.conf import settings
# from django.contrib.auth import get_user_model
# import stripe

# User = get_user_model()

# stripe.api_key = settings.STRIPE_SECRET_KEY

# @method_decorator(login_required, name='dispatch')
# class AddPaymentMethodView(View):
#     template_name = 'payment.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         payment_method_id = request.POST.get('payment_method_id')
#         shipping_name = request.POST.get('shipping_name')
#         shipping_address = request.POST.get('shipping_address')
#         shipping_city = request.POST.get('shipping_city')
#         shipping_country = request.POST.get('shipping_country')
#         shipping_state = request.POST.get('shipping_state')

#         try:
#             # Create a new customer in Stripe
#             customer = stripe.Customer.create(
#                 payment_method=payment_method_id,
#                 email=request.user.email,
#                 invoice_settings={
#                     'default_payment_method': payment_method_id
#                 }
#             )

#             # Attach the PaymentMethod to the customer
#             stripe.PaymentMethod.attach(
#                 payment_method_id,
#                 customer=customer.id
#             )

#             # Modify the billing details of the PaymentMethod
#             stripe.PaymentMethod.modify(
#                 payment_method_id,
#                 billing_details={
#                     'name': shipping_name,
#                     'address': {
#                         'line1': shipping_address,
#                         'city': shipping_city,
#                         'country': shipping_country,
#                         'state': shipping_state
#                     }
#                 }
#             )
#             request.user.payment_method_id = payment_method_id
#             request.user.save()

#             return render(request, self.template_name, {'success': True})
#         except stripe.error.InvalidRequestError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
        
# class ProcessPaymentView(View):
#     template_name = 'payment.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         try:
#             payment_method_id = request.user.payment_method_id

#             # Create a payment intent
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=2000,  # Adjust the amount as needed
#                 currency="usd",
#                 payment_method=payment_method_id,
#                 confirmation_method='manual',
#                 confirm=True,
#             )

#             # Check the status of the payment intent
#             if payment_intent['status'] == 'succeeded':
#                 # Payment was successful
#                 return render(request, 'success.html', {'success': True})
#             else:
#                 # Payment failed
#                 return render(request, 'failure.html', {'error': 'Payment failed'})

#         except stripe.error.InvalidRequestError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)


# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from django.conf import settings
# from django.views import View
# import stripe
# from authenticate.models import User
# from orderapp.models import Order
# from payment.models import Payment

# stripe.api_key = settings.STRIPE_SECRET_KEY

# class CheckoutView(View):
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
    
#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get('user_id')
#         user = User.objects.get(id=user_id)
#         order_ids = request.GET.getlist('order_ids[]') 
#         orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
#         total_amount = 0
#         for order_id in order_ids:
#             order = Order.objects.get(pk=order_id)
#             products = order.cart.products.all()  
#             order_amount = sum(product.price for product in products)
#             total_amount += order_amount
#         context = {
#             'user': user,
#             'orders': orders,
#             'total_amount': total_amount,
#         }
#         request.session['order_ids'] = order_ids
#         return render(request, 'pay.html', context)


#     def post(self, request,*args,**kwargs):
#         user_id = kwargs.get('user_id')
#         user = User.objects.get(id=user_id)
#         order_ids = request.session.get('order_ids', [])
#         payment_method_id = request.POST.get('paymentMethodId')
#         currency = 'usd'
#         shipping_name = request.POST.get('shippingName') 
#         shipping_address = request.POST.get('shippingAddress')
#         shipping_city = request.POST.get('shippingCity')
#         shipping_country = request.POST.get('shippingCountry')
#         shipping_state = request.POST.get('shippingState')

#         try:
#             total_amount = 0 
#             payment_intent_items = []

#             for order_id in order_ids:
#                 order = Order.objects.get(pk=order_id)
#                 products = order.product.all()  
#                 order_amount = sum(product.price for product in products)
#                 total_amount += order_amount  
#                 for product in products:
#                     payment_intent_items.append({
#                         'amount': product.price * 100,  # Amount in cents
#                         'currency': currency,
#                         'description': product.name,
#                         'quantity': 1, 
#                     })
#             print(payment_intent_items)
#             # Create or retrieve a customer in Stripe
#             customer = stripe.Customer.create(
#                 name=user.first_name,
#                 email=user.email,
#             )
            
#             stripe.PaymentMethod.attach(
#                 payment_method_id,
#                 customer=customer.id
#             )
            
#             stripe.PaymentMethod.modify(
#                 payment_method_id,
#                 billing_details={
#                     'name': shipping_name,
#                     'address': {
#                         'line1': shipping_address,
#                         "city": shipping_city,
#                         "country": shipping_country,
#                         "state": shipping_state
#                     }
#                 }
#             )
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(float(total_amount) * 100),
#                 currency=currency,
#                 customer=customer.id,
#                 payment_method=payment_method_id,
#                 description=f"Payment for multiple orders: {payment_method_id}",
                
#                 # metadata={'order_ids': str(order_ids)},
#             )

#             payment = Payment.objects.create(user=user,amount_paid=total_amount, client_secret=payment_intent.client_secret)
#             payment.save()
#             client_secret = payment_intent.client_secret
#             request.session['order_ids'] = order_ids
#             request.session['client_secret'] = payment_intent.client_secret
#             request.session['payment_id']= payment.id
#             # return JsonResponse({'client_secret': client_secret}, status=200)
#             return redirect('pay_for_checkout', user_id=user_id)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)
#         except stripe.error.StripeError as e:
#             return JsonResponse({'error': str(e)}, status=500)
        

# class PayForCheckoutView(View):
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request,*args,**kwargs):
#         client_secret = request.session.get('client_secret','')
#         payment_id = request.session.get('payment_id',0)
#         user_id = kwargs.get('user_id')
#         user = User.objects.get(id=user_id)
#         orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
#         order_ids = request.session.get('order_ids', [])
#         orders = Order.objects.filter(id__in=order_ids)
#         total_amount = 0
#         for order_id in order_ids:
#                 order = Order.objects.get(pk=order_id)
#                 products = order.product.all()
#                 # Calculate total amount for the order
#                 order_amount = sum(product.price for product in products)
#                 total_amount += order_amount
#         context = {
#             'client_secret': client_secret,
#             'user': user,
#             'orders': orders,
#             'total_amount': total_amount,
#             'payment_id': payment_id
#         }
#         return render(request, 'payment.html',context) 

# class PaymentSuccessView(View):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     def get(self, request, *args, **kwargs):
#         payment_id = kwargs.get('payment_id')
#         payment = get_object_or_404(Payment, pk=payment_id)
#         payment.is_paid = True
#         payment.save()
#         return render(request, 'success.html')
