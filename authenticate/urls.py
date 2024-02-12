from django.urls import path
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView, UserProfileView, UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns=[
    path('register/', UserRegistrationView.as_view() ,name='register'),
    path('login/', UserLoginView.as_view() ,name='login'),
    path('profile/', UserProfileView.as_view() ,name='profile'),
    path('changepassword/', UserChangePasswordView.as_view() ,name='changepassword'),
    path('resetforgotpassword/',SendPasswordResetEmailView.as_view(), name='reset_forgot_password'),
    path('resetpassword/<uid>/<token>/',UserPasswordResetView.as_view(), name='reset_password'), 
    path('logout/',UserLogoutView.as_view(), name='logout'),
]
