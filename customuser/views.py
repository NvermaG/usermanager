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

# Create your views here.

User = get_user_model()


class RegisterApi(ModelViewSet):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    # view_permissions = {
    #     'retrieve': {'user': is_self, 'admin': True},
    #     'create': {'anon': True},
    #     'list': {'admin': True},
    # }

    # @allowed('anon', 'admin')
    @transaction.atomic
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = RegisterUserSerializer.create(self, serializer.data)
        user = serializer.save()
        user.set_password(serializer.data.get('password'))
        user.save()
        return Response("You are registered")


class UserApi(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]

    # @allowed('admin', 'anon', 'user')
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    # @allowed('admin')
    @transaction.atomic
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = User.create(self, serializer.data)
        user = serializer.save()
        user.set_password(settings.EMAIL_DEFAULT_PASSWORD)
        user.save()
        return Response("User Created Successfully")

    # @allowed('user', 'admin')
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


@method_decorator(name="change_password", decorator=UserSwagger.change_password())
class UserChangePassword(ModelViewSet):
    # serializer_class = ChangeUserPassword
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(is_active=True)

    def get_password(self):
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        return old_password, new_password

    def change_password(self, request):
        old_password, new_password = self.get_password()
        request.user.change_password(old_password, new_password)
        return Response("Password successfully changed")














        # self.object = self.get_object()
        # user = self.request.user
        # serializer = self.get_serializer(data=request.data)
        # flag = "Change"
        # if serializer.is_valid():
        #     response = user.resetandchangepass(serializer.data, flag)
        #     return Response(response)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(ModelViewSet):
    serializer_class = ResetUserPasswordSerializer
    model = User


    # @allowed('anon')
    @transaction.atomic
    def post(self, request):
        # if self.request.user.is_superuser and self.request.user.is_anonymous:
        #     return Response("You do not have permission to perform this action.")
        # else:
        serializer = self.get_serializer(data=request.data)
        flag = "Reset"
        serializer.is_valid()
        response = User.Resetandchangepass(self, serializer.data, flag)
        return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
