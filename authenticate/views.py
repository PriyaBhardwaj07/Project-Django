from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SendPasswordResetEmailSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserChangePasswordSerializer
from django.contrib.auth  import authenticate
from .renderers import UserRenderer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    
    renderer_classes =[UserRenderer, TemplateHTMLRenderer]
    template_name = 'registration.html'
    
    def get(self, request, format=None):
        reg_form = UserRegistrationSerializer()
        return Response({'reg_form': reg_form}, template_name=self.template_name)
    
    def post(self, request, format = None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return redirect('login')
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    
    renderer_classes =[UserRenderer, TemplateHTMLRenderer]
    template_name = 'login.html'
    
    def get(self, request, format=None):
        login_form = UserLoginSerializer()
        return Response({'login_form': login_form}, template_name=self.template_name)
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user=authenticate(email=email, password=password) 
            if user is not None:
                token = get_tokens_for_user(user)
                return redirect('home')
            else:
                return Response({'errors':{'non_field_errors': ['Email or Password is not valid']}}, status = status.HTTP_404_NOT_FOUND)
            

class UserProfileView(APIView):
    renderer_classes = [UserRenderer,TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated] 
    def get(self,request, format=None):
        serializer = UserProfileSerializer(request.user) 
        return Response({"profile":serializer.data}, status = status.HTTP_200_OK, template_name='profile.html')

class UserChangePasswordView(APIView):  
    renderer_classes = [UserRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated] 
    template_name = 'changepassword.html'    
    def get(self, request, format=None):
        change_password_form = UserChangePasswordView()
        return Response({'login_form': change_password_form}, template_name=self.template_name)   
    def post(self, request, format =None):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception =True):
            return Response({'msg':'Password Changed Successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link is sent. please check your email'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data = request.data, context={'uid':uid,'token':token })
        if serializer.is_valid(raise_exception =True):
            return Response({'msg':'Password has been reset'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request, format = None):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"success": "User logged out successfully."}, status=status.HTTP_200_OK)
                return redirect('login')
            else:
                return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
