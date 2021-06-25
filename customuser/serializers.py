
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User



User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }



    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        subject = 'Welcome to our UserManagement'
        message = f'Hi {user.username}, thank you for registering in UserManagement Project.'
        recipient_list = [user.email]
        User.mailsent = classmethod(User.mailsent)
        User.mailsent(subject, message, recipient_list)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }




class ChangeUserPassword(serializers.ModelSerializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']


class ResetUserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'old_password', 'new_password']

