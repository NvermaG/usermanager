from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
# from rest_framework_roles.decorators import allowed
from django.conf import settings
from .serializers import RegisterUserSerializer, ChangeUserPassword, UserSerializer, ResetUserPasswordSerializer
# from rest_framework_roles.granting import is_self
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework import status
from django.db import transaction
# from .models import User
from django.utils.decorators import method_decorator
from .swagger import UserSwagger
from django.conf import settings
from .managers import otp_authentication

# Create your views here.

User = get_user_model()


class RegisterApi(ModelViewSet):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    # Anonymous user and Super User can Register
    @transaction.atomic
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = RegisterUserSerializer.create(self, serializer.data)
        user = serializer.save()
        user.set_password(serializer.data.get('password'))
        message = f"Hello {user.username}, thank you for registration in project"
        user.mail_sent(message)
        user.save()
        return Response("You are registered")


class UserApi(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    # Only Authenticated user can fetch the record of users
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("you don't have permission to access data")

    # Only Super User can create user
    @transaction.atomic
    def create_user(self, request):
        if request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # user = User.create(self, serializer.data)
            user = serializer.save()
            message = f"Hello {user.username},default password is {settings.EMAIL_DEFAULT_PASSWORD}"
            user.mail_sent(message)
            user.set_password(settings.EMAIL_DEFAULT_PASSWORD)
            user.save()
            return Response("User Created Successfully")
        else:
            return Response("you don't have permission to access data")

    # Only Authenticated user can update record
    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("you don't have permission to access data")


@method_decorator(name="change_password", decorator=UserSwagger.change_password())
class UserChangePassword(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(is_active=True)

    def get_password(self):
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        return old_password, new_password

    #Authenticated user can change the password
    @transaction.atomic
    def change_password(self, request):
        user = request.user
        if user.is_authenticated:
            old_password, new_password = self.get_password()
            response = request.user.change_password(old_password, new_password)
            message = f"Hello {user.username}, you successfully changed your password"
            user.mail_sent(message)
            return Response(response)
        else:
            return Response("you don't have permission to access data")


@method_decorator(name="reset_password", decorator=UserSwagger.reset_password())
@method_decorator(name="forget_password", decorator=UserSwagger.forget_password())
class UserResetPasswordView(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.filter(is_active=True)

    def get_email(self):
        email = self.request.data.get('Email')
        return email

    ''' 
        if registered user forget his password then they can reset his password by 
        entering his email id and get the otp at mail after they will reset the password  
    '''

    @transaction.atomic
    def forget_password(self, request):
        if not request.user.is_authenticated:
            email = self.get_email()
            user = User.objects.get(email=email)
            user.otp = otp_authentication()
            message = f"Hello {user.username}, your one time password is {user.otp}"
            user.mail_sent(message)
            user.save()
            return Response("OTP Generate Successfully")
        else:
            return Response("You are logged In")

    # registered user can reset password via otp
    @transaction.atomic
    def reset_password(self, request):
        if not request.user.is_authenticated:
            email = self.get_email()
            user = User.objects.get(email=email)
            otp = self.request.data.get('otp')
            password = self.request.data.get('new_password')
            if user.otp == otp:
                response = user.reset_password(password)
                message = f"Hello {user.username}, your password reset successfully"
                user.mail_sent(message)
                user.otp = otp_authentication()
                user.save()
                return Response(response)
            else:
                return Response("Invalid Otp")
        else:
            return Response("You are logged In")