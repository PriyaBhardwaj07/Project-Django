from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from authenticate.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from productapp.models import Product
from .models import Cart, CartItems, SaveForLater

class CartView(LoginRequiredMixin, View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')  
        try:
            cart = Cart.objects.get(user_id=user_id)
            cart_items = cart.cart_items.select_related('products')
            context = {'cart_items': cart_items, 'user_id': user_id}
        except Cart.DoesNotExist:
            context = {'cart_empty': True}
        return render(request, self.template_name, context)

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            user = get_object_or_404(User, id=user_id)
            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(user=user)
            cart_item, created = CartItems.objects.get_or_create(cart=cart, products=product)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            return JsonResponse({'message': 'Product added to cart.'}, status=201)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity value.'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DeleteFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            cart = get_object_or_404(Cart, user_id=user_id)
            product = get_object_or_404(Product, id=product_id)
            cart_item = get_object_or_404(CartItems, cart=cart, products=product_id)
            quantity = cart_item.quantity
            cart_item.delete()
            product.quantity += quantity
            product.save()
            return JsonResponse({'message': 'Product removed from cart.'}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found.'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except CartItems.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class TransferToSaveForLaterView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            user = get_object_or_404(User, id=user_id)
            product = get_object_or_404(Product, id=product_id)
            cart = get_object_or_404(Cart, user=user)
            cart_item = get_object_or_404(CartItems, cart=cart, products=product)
            save_for_later, created = SaveForLater.objects.get_or_create(user_id=user)
            save_for_later.products_id.add(product)
            product.quantity += cart_item.quantity
            product.save()
            cart_item.delete()
            return JsonResponse({'message': 'Product transferred to Save For Later'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found.'}, status=404)
        except CartItems.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DeleteFromWishListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            wish_cart = get_object_or_404(SaveForLater, user_id=user_id)
            product = get_object_or_404(Product, id=product_id)
            item = SaveForLater.objects.filter(user_id=user_id, products_id=product).first()
            if item:
                item.delete()
                return JsonResponse({'message': 'Product removed from Wishlist.'}, status=200)
            else:
                return JsonResponse({'error': 'Product not found in Wishlist.'}, status=404)
        except SaveForLater.DoesNotExist:
            return JsonResponse({'error': 'Cart not found.'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class TransferFromSaveForLaterToCartView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            
            user = get_object_or_404(User, id=user_id)
            product = get_object_or_404(Product, id=product_id)
            cart = get_object_or_404(Cart, user=user)
            
            save_for_later=get_object_or_404(SaveForLater, user_id=user)
            save_for_later.products_id.remove(product)   
            
            cart_item, created = CartItems.objects.get_or_create(cart=cart, products=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()
            return JsonResponse({'message': 'Product transferred to Cart'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except SaveForLater.DoesNotExist:
            return JsonResponse({'error': 'Cart not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class WishListView(LoginRequiredMixin, View):
    template_name = 'wishlist.html'
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            wish_cart = SaveForLater.objects.get(user_id=user_id)
            cart_items = wish_cart.products_id.all()
            context = {'cart_items': cart_items, 'user_id': user_id}
        except SaveForLater.DoesNotExist:
            context = {'cart_empty': True, 'cart_items': [], 'user_id': user_id}
        return render(request, self.template_name, context)
