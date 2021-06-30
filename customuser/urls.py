from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import RegisterApi, UserChangePassword, UserApi, UserResetPasswordView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('Register/api/', RegisterApi.as_view({'post': 'register'})),
    path('api/', UserApi.as_view({'post': 'create_user'})),
    path('api/retrieve', UserApi.as_view({'get': 'get'})),
    path('reset/passwd', UserResetPasswordView.as_view({'post': 'post'})),
    path('<int:pk>/update/api/', UserApi.as_view({'patch': 'patch'})),
    path('<int:pk>/delete/api', UserApi.as_view({'delete': 'destroy'})),
    path('Change/password', UserChangePassword.as_view({'post': 'change_password'})),
    path('forget/password', UserResetPasswordView.as_view({'post': 'forget_password'})),
    path('Reset/password', UserResetPasswordView.as_view({'post': 'reset_password'})),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    ]