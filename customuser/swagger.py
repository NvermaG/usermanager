from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class UserSwagger:
    @staticmethod
    def change_password():
        doc = swagger_auto_schema(
            tags=["user"],
            operation_summary="Reset password by passing old password",
            operation_description="Reset password by passing old password",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Old Password'),
                    'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New Password'),
                }),
            responses={status.HTTP_200_OK: _("Your password has been changed successfully.")}
        )
        return doc