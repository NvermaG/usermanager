from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from django.contrib.auth.models import AbstractBaseUser



class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


    # def passwdreset(self, validated_data, old_password, new_password):
    #     obj = User.objects.get(email=validated_data['email'])
    #     print(self.queryset)
    #     if obj.check_password(old_password):
    #         return Response("You old password is not correct")
    #     obj.set_password(new_password)
    #     print("yes")
    #     self.obj.save()
    #     return Response("Password Reset successfully")