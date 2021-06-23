from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer
User = get_user_model()

# Create your views here.

class RegisterApi(ModelViewSet):
    serializer_class = RegisterUserSerializer
    http_method_names = ["get", "post", "put", "delete","patch"]

    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterUserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })