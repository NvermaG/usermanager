from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework_roles.decorators import allowed
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterUserSerializer, ChangeUserPassword, UserSerializer, ResetUserPasswordSerializer
# from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework_roles.granting import is_self
from rest_framework import status
from django.db import transaction
from .models import User


from django.contrib.auth.models import AbstractBaseUser
# Create your views here.

User = get_user_model()


class RegisterApi(ModelViewSet):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    view_permissions = {
        'retrieve': {'user': is_self, 'admin': True},
        'create': {'anon': True},
        'list': {'admin': True},
    }

    @allowed('anon', 'admin')
    @transaction.atomic
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = RegisterUserSerializer.create(self, serializer.data)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response("You are registered")


class UserApi(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    @allowed('admin', 'anon', 'user')
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @allowed('admin')
    @transaction.atomic
    def createuser(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.create(self, serializer.data)
        user.set_password(settings.EMAIL_DEFAULT_PASSWORD)
        user.save()
        return Response("User Created Successfully")

    @allowed('user', 'admin')
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserChangePassword(ModelViewSet):
    serializer_class = ChangeUserPassword
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @allowed('anon', 'admin')
    def changepasswd(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(ModelViewSet):
    serializer_class = ResetUserPasswordSerializer
    # permission_classes = (AllowAny,)
    model = User

    @allowed('user', 'admin')
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        queryset = User.objects.get(email=serializer.data.get('email'))
        if not queryset.check_password(serializer.data.get("old_password")):
            return Response("wrong passwd")
        if old_password == new_password:
            return Response("New password and old password could not be same")
        queryset.set_password(serializer.data.get("new_password"))
        queryset.save()
        return Response("successfully reset")






        # if queryset:
        #     request.user.passwdreset(serializer.data, old_password, new_password)
        # else:
        #     return Response("These data does not exist")

        # return Response("successfully")


