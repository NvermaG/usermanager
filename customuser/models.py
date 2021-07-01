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

    def mail_sent(self, message=None):
        email_from = settings.EMAIL_HOST_USER
        subject = 'Welcome to our UserManagement'
        recipient_list = [self.email]
        send_mail(subject, message, email_from, recipient_list)
        return True

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
