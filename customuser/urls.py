from django.urls import path
from .views import RegisterApi, UserChangePassword, UserApi, UserResetPasswordView

urlpatterns = [
    path('Register/api/', RegisterApi.as_view({'post': 'register'})),
    path('api/', UserApi.as_view({'post': 'createuser'})),
    path('api/retrieve', UserApi.as_view({'get': 'get'})),
    path('reset/passwd', UserResetPasswordView.as_view({'post': 'post'})),
    path('<int:pk>/update/api/', UserApi.as_view({'patch': 'patch'})),
    path('<int:pk>/delete/api', UserApi.as_view({'delete': 'destroy'})),
    path('Change/password', UserChangePassword.as_view({'post': 'changepasswd'})),
    path('<int:pk>/password', UserChangePassword.as_view({'post': 'changepasswd'}))
    ]