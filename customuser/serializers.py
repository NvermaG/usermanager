
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], password=validated_data['password'],
                                            email=validated_data['email'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'])
            return user

class ChangeUserPassword(serializers.ModelSerializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['old_password', 'new_password']

