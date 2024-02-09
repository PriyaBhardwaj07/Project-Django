from django.contrib import admin
from django.urls import include, path

from .views import index , signup

urlpatterns = [
    path('',index,name='homepage'),
    path('signup',signup),
    #path('signup/', signup, name='signup'),
    
    path('api/user/',include('authenticate.urls'))
    
]
