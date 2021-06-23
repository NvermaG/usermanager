from django.urls import path
from .views import RegisterApi,UserChangePassword
urlpatterns = [
    path('Register/api/', RegisterApi.as_view({'post': 'register'})),
    path('api/', RegisterApi.as_view({'post':'createuser'})),
    path('api/retrieve', RegisterApi.as_view({'get':'get'})),
    path('<int:pk>/update/api/', RegisterApi.as_view({'patch':'patch'})),
    path('<int:pk>/delete/api',RegisterApi.as_view({'delete':'destroy'})),
    path('Reset/password',UserChangePassword.as_view({'post':'changepasswd'}))
    ]