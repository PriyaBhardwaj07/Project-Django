from django.urls import path, include
from authenticate.views import UserLoginView, UserRegistrationView
from django.conf.urls.static import static


urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    
]