from django.urls import path
from . import views


urlpatterns=[
    path('home/',views.Home.as_view(), name='home'),
    path('product/<int:pk>/',views.ProductDetail.as_view(), name='productdetail'),
    path('product_filter/',views.ProductFilterView.as_view(), name='product_filter'),

]
