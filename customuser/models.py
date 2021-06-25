from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def mailsent(self, subject, message, recipient_list=None):
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        return True

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        subject = 'Welcome to our UserManagement'
        message = f'Hi {user.username}, thank you for join us in UserManagement Project.And Your default password is {settings.EMAIL_DEFAULT_PASSWORD}, kindly login and Change the password'
        recipient_list = [user.email]
        User.mailsent = classmethod(User.mailsent)
        User.mailsent(subject, message, recipient_list)
        return user


    # def passwdreset(self, validated_data, old_password, new_password):
    #     obj = User.objects.get(email=validated_data['email'])
    #     print(self.queryset)
    #     if obj.check_password(old_password):
    #         return Response("You old password is not correct")
    #     obj.set_password(new_password)
    #     print("yes")
    #     self.obj.save()
    #     return Response("Password Reset successfully")