from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class UserSwagger:
    @staticmethod
    def change_password():
        doc = swagger_auto_schema(
            tags=["user"],
            operation_summary="Change password by passing old password",
            operation_description="Change password by passing old password",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Old Password'),
                    'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New Password'),
                }),
            responses={status.HTTP_200_OK: _("Your password has been changed successfully.")}
        )
        return doc

    @staticmethod
    def reset_password():
        doc = swagger_auto_schema(
            tags=["user"],
            operation_summary="Reset password by passing OTP",
            operation_description="Reset password by passing OTP",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'otp': openapi.Schema(type=openapi.TYPE_STRING, description='otp'),
                    'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New Password'),
                }),
            responses={status.HTTP_200_OK: _("Your password has been changed successfully.")}
        )
        return doc

    @staticmethod
    def forget_password():
        doc = swagger_auto_schema(
            tags=["user"],
            operation_summary="Generate OTP by passing email",
            operation_description="Generate OTP by passing email",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                }),
            responses={status.HTTP_200_OK: _("Successfully OTP sent to your registered Email Id")}
        )
        return doc
