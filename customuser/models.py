import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError

from .managers import check_validation


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    otp = models.CharField(max_length=10, null=True)

    def mail_sent(self, subject, message, recipient_list=None):
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
        # subject = 'Welcome to our UserManagement'
        # message = f'Hi {user.username}, thank you for join us in UserManagement Project.And Your default password is {settings.EMAIL_DEFAULT_PASSWORD}, kindly login and Change the password'
        # recipient_list = [user.email]
        # User.mailsent = classmethod(User.mailsent)
        # User.mailsent(subject, message, recipient_list)
        return user

    def validate_password(self, old_password, new_password):
        if not check_validation(new_password):
            raise ValidationError("Invalid New Password")

        elif old_password == new_password:
            raise ValidationError('old password and new password could not be same')

        elif not self.check_password(old_password):
            raise ValidationError('old password did not match')

    def set_password_with_confirmation(self, new_password):
        self.set_password(new_password)
        self.save()
        return True

    def change_password(self, old_password, new_password):
        self.validate_password(old_password, new_password)
        self.set_password_with_confirmation(new_password)
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }
        return response

    def reset_password(self, password):
        if not check_validation(password):
            raise ValidationError("Invalid New Password")
        self.set_password_with_confirmation(password)
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password reset successfully',
            'data': []
        }
        return response
