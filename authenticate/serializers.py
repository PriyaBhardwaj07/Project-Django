from xml.dom import ValidationErr
from rest_framework import serializers
from authenticate.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from authenticate.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)  # Remove 'password2' from validated_data
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        user.set_password(password)
        user.save()
        return attrs
""" 
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email   = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email=email)
            # this below encode method take data in the form of byte rather than int 
            # also we are using this method because we don't want the id directly it should be encoded
            # for protection
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print("Password Reset Link",link)
            # Send Email
            body = 'Click the link to reset your password'+ link
            data={
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')
"""
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            print('Encoded UID', uid)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            print("Password Reset Link", link)

            # Send Email
            body = 'Click the link to reset your password: ' + link
            data = {
                'subject': 'Reset your password',  # Removed extra space here
                'body': body,
                'to_email': user.email
            }

            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')



class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        # we are writing this in try-except for extra protection
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            # we are writing this because we have to get the user here from serializers
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password don't match")
            # smart_str is used to get the value in a string
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not valid or expired')           
