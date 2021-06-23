from django.urls import path
from .views import RegisterApi
urlpatterns = [
    path('Register/api/', RegisterApi.as_view({'post': 'register'}))
    ]