# from django.urls import path
# from .views import AddPaymentMethodView, ProcessPaymentView

# urlpatterns = [
#     path('add_payment_method/', AddPaymentMethodView.as_view(), name='add_payment_method'),
#     path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    
#     # Add more URL patterns as needed
# ]
# from django.urls import path
# from .views import   CheckoutView, PaymentSuccessView, PayForCheckoutView
# urlpatterns=[
#     path('payment_success/<int:payment_id>/',PaymentSuccessView.as_view(),name='successful_payment_page'),
#     path('checkout/<int:user_id>', CheckoutView.as_view(), name='checkout'),
#     path('pay_for_checkout/<int:user_id>', PayForCheckoutView.as_view(), name='pay_for_checkout'),
    
    
    
    
# ]

from django.urls import path
from .views import   CheckoutView, PaymentSuccessView, PayForCheckoutView, PaymentListView, PaymentRefundView
urlpatterns=[
    path('payment_success/<int:payment_id>/',PaymentSuccessView.as_view(),name='successful_payment_page'),
    path('checkout/<int:user_id>', CheckoutView.as_view(), name='checkout'),
    path('pay_for_checkout/<int:user_id>', PayForCheckoutView.as_view(), name='pay_for_checkout'),
    path('payments_display/<int:user_id>', PaymentListView.as_view(), name='payments_display'),
    path('payment_refund/<int:user_id>', PaymentRefundView.as_view(), name='payment_refund'),
    
    
    
    
    
    
]