"""
from rest_framework import serializers
from authenticate.models import User

class UserRegistrationSerializers(serializers.ModelSerializer):
    # we are writing here because we need to confirm the password field in our Registration request
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields=['email','name','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
        # VALIDATE PASSWORD AND CONFIRM PASSWORD
        
        def validate(self,attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')  
            if password != password2:
                raise serializers.ValidationError("Password doesn't match")
            return attrs
        
        def create(self,validate_data):
            
            return User.objects.create_user(**validate_data)

    def create(self, validated_data):
        # Remove 'password2' from validated_data before calling create_user
        validated_data.pop('password2', None)
        return User.objects.create_user(**validated_data)
"""
from rest_framework import serializers
from authenticate.models import User

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
        