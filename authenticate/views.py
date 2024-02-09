from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from authenticate.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from authenticate.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from authenticate.utils import Util

# to generate tokens manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({'tokens': tokens, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response({'tokens': tokens, 'msg': 'Login Successful'}, status=status.HTTP_200_OK) 
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# non field errors: if the combination of email and password doesn’t
# match any existing user during login, that’s a non-field error.

class UserProfileView(APIView):
    renderer_classes =[UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
 
class UserChangePasswordView(APIView):
    renderer_classes =[UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data= request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Changed'}, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           return Response({'msg':'Password Reset Link sent. Please check your email'},status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email_data = {
                'email_subject': 'Your Reset Password Subject',  # Provide a subject here
                'body': 'Your email body content',  # Provide the email body content here
                'to_email': serializer.validated_data['email'],
            }
            Util.send_email(email_data)
            return Response({'msg': 'Password Reset Link sent. Please check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


           
class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

