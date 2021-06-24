from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer, ChangeUserPassword, UserSerializer, ResetUserPasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import status
from .models import User

from django.contrib.auth.models import AbstractBaseUser
# Create your views here.

User = get_user_model()


class RegisterApi(ModelViewSet, AbstractBaseUser):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = RegisterUserSerializer.create(self, serializer.data)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response("You are registered")


class UserApi(ModelViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, AbstractBaseUser):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def createuser(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
        )
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response("User Created Successfully")

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserChangePassword(ModelViewSet):
    serializer_class = ChangeUserPassword
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user

        return obj

    def changepasswd(self, request, *args, **kwargs):
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
    permission_classes = (IsAuthenticated,)
    model = User

    def post(self, request, *args, **kwargs):
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


