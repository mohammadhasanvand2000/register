from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', method_decorator(csrf_exempt)(views.UserRegistrationView.as_view()), name='register'),
    path('login/',  method_decorator(csrf_exempt)(views.UserLoginView.as_view()), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
  
]
