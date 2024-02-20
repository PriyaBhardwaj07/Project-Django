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
            
#             # Optionally, save the payment method ID to your user's profile
#             # request.user.payment_method_id = payment_method_id
#             # request.user.save()

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
#         # Return error response if the request method is not POST
#         return render(request, 'success.html', {'payment_intent': None})


from django.shortcuts import render
from django.http import JsonResponse
import stripe
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
import stripe

stripe.api_key = 'sk_test_51OkIzmSGCDrMJpDVDDm6L0HgAtHdB2VNSB9MymLtDJhrQM28GSInbhT3Vqw1DsdZd6cgbK19ZGTNWz7Im5OCZGxM00uj1QQ0O9'

def add_payment_method(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')
        
        try:
            # Create a new customer in Stripe
            customer = stripe.Customer.create(
            payment_method=payment_method_id,
            email=request.user.email,  # Assuming you have a user object
            invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
            
            # Optionally, save the payment method ID to your user's profile
            # CHECK THESE 2 LINES ,,,,,,,,,,,,
            request.user.payment_method_id = payment_method_id
            request.user.save()
            
            # Render payment.html template with success message
            return render(request, 'payment.html', {'success': True})
        except stripe.error.InvalidRequestError as e:
            # Return error response if the payment method ID is invalid
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Return error response for other exceptions
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Render the payment_form.html template for GET requests
        return render(request, 'payment.html')

def process_payment(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')

        try:
            # Confirm the payment with Stripe
            payment_intent = stripe.PaymentIntent.create(
               # Adjust amount as needed (in cents)
                amount=2000,
                currency="usd",
                automatic_payment_methods={"enabled": True},
                payment_method_types=["card"],

)
            # Save payment information to database (optional)
            # Example: Payment.objects.create(payment_method_id=payment_method_id, user=request.user)

            # Send email notification
            # send_mail(
            #     'Payment Successful',
            #     'Your payment was successful.',
            #     'bhardwajpriya2002@gmail.com',  # Replace with sender email
            #     ['bhardwajpriay@gmail.com'],  # Replace with recipient email
            #     fail_silently=False,
            # )

            # Render payment confirmation template
            return render(request, 'success.html', {'payment_intent': payment_intent})
        except stripe.error.StripeError as e:
            # Handle payment failure
            return render(request, 'failure.html', {'error': str(e), 'payment_intent': None})

    else:
      payment_intent = stripe.PaymentIntent.create(
               # Adjust amount as needed (in cents)
                amount=2000,
                currency="usd",
                automatic_payment_methods={"enabled": True},)
               
        # Return error response if request method is not POST
      return render(request, 'success.html', {'payment_intent': payment_intent})
  
  
  