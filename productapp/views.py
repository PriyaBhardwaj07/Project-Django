from django.shortcuts import render
from django.views.generic import ListView, DetailView
from orderapp.models import FeedBack
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

# class HomeLast(ListView): # error check in this 
#     model = Product
#     template_name = 'home.html'
#     context_object_name = 'products' 
    
#     def get_queryset(self):
#         sort_by = self.request.GET.get('sort')
#         if sort_by == 'new_arrival':
#             queryset = Product.objects.order_by('-id')
#         elif sort_by == 'from_oldest':
#             queryset = Product.objects.order_by('id')
#         elif sort_by == 'price_max_to_low':
#             queryset = Product.objects.order_by('-price')
#         elif sort_by == 'price_low_to_max':
#             queryset = Product.objects.order_by('price')
#         else:
#             queryset = Product.objects.all()
#         return queryset

    
class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        product = self.object
        feedbacks = FeedBack.objects.filter(product_id=product)
        context['feedbacks'] = feedbacks
        context['user_id'] = user_id
        context['stars_range'] = range(5)
        return context
    

class Home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products' 
    
    def get_queryset(self):
        sort_by = self.request.GET.get('sort')
        if sort_by == 'new_arrival':
            queryset = Product.objects.order_by('-id')
        elif sort_by == 'from_oldest':
            queryset = Product.objects.order_by('id')
        elif sort_by == 'price_max_to_low':
            queryset = Product.objects.order_by('-price')
        elif sort_by == 'price_low_to_max':
            queryset = Product.objects.order_by('price')
        else:
            queryset = Product.objects.all()
        return queryset

class ProductFilterView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')  
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset