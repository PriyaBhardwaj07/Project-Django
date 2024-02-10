"""
from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, product_detail

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail-api'),
    path('products/<int:pk>/detail/', product_detail, name='product-detail'),
]
"""

from django.urls import path
from . import views


urlpatterns=[
    path('',views.Home.as_view(), name='home'),
    path('product/<int:pk>/',views.ProductDetail.as_view(), name='productdetail'),
    path('product_filter/',views.ProductFilterView.as_view(), name='product_filter'),

]
