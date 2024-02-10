from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from authenticate.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from productapp.models import Product
from .models import Cart, SaveForLater


# Create your views here.

class CartView(LoginRequiredMixin,View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')  
        cart_items = Cart.objects.filter(user_id=user_id).prefetch_related('products_id')
        context = {}
        if cart_items.exists():
            context['cart_items'] = cart_items
        else:
            context['cart_empty'] = True
        return render(request, self.template_name, context)
    

class AddToCartView(LoginRequiredMixin,View):
    
    template_name ='addcart.html'
    context_object_name = 'cart_items'
    
    def post(self, request, *args, **kwargs):
        user_id_ = kwargs.get('user_id')
        product_id_ = kwargs.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        user = get_object_or_404(User, id=user_id_)
        if not all([product_id_ , user_id_ ]):
            return JsonResponse({'error': 'User ID and Product ID are required.'}, status=400)      
        cart, created =Cart.objects.get_or_create(user_id = user)
        
        if cart.products_id.filter(id=product_id_ ).exists():
            cart_item = cart.products_id.get(id=product_id_ )
            cart_item.quantity +=quantity
            cart_item.save()
            return JsonResponse({'message': 'Quantity updated in cart.'}, status=200)
        
        #if it is new item for cart of current user
        product = get_object_or_404(Product, id=product_id_ )
        cart.products_id.add(product, through_defaults={'quantity': quantity})
        return JsonResponse({'message': 'Product added to cart.'}, status=201)
    
class DeleteFromCartView(LoginRequiredMixin,View):
    
    template_name ='cart.html'
    context_object_name = 'cart_items'
    
    def post(self, request, *args, **kwargs):
        user_id_ = request.POST.get('user_id')
        product_id_ = request.POST.get('product_id')
        
        if not all[product_id_ , user_id_ ]:
            return JsonResponse({'error': 'User ID and Product ID are required.'}, status=400)
        
        product = Cart.objects.get(id=product_id_ )
        
        if not product.products_id.filter(id = product_id_ ).exists():
            return JsonResponse({'error': 'Product is not in the cart.'}, status=404)
        
        cart_item = product.product_id.get(id=product_id_ )
        quantity = cart_item.quantity
        product.product_id.remove(cart_item)
        
        product.quantity -= quantity
        product.save()
        return JsonResponse({'message': 'Product removed from cart.'}, status=200)
    
class TransferToSaveForLaterView(View):
    
    template_name ='cart.html'
    context_object_name = 'cart_items'
    
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)
        
        save_for_later, created = SaveForLater.objects.get_or_create(user_id=user_id)
        
        if not created and save_for_later.products_id.filter(id=product_id).exists(): 
            save_for_later.products_id.set([product_id])
            save_for_later.quantity = quantity
            save_for_later.save()
            return JsonResponse({'message': 'Product quantity updated in Save For Later'}, status=200)
        
        save_for_later.products_id.add(product_id)
        save_for_later.quantity = quantity
        save_for_later.save()
        return JsonResponse({'message': 'Product added to Save For Later'}, status=201)