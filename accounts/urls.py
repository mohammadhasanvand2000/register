from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

urlpatterns = [
    path('register/', method_decorator(csrf_exempt)(views.UserRegistrationAPIView.as_view()), name='register'),
    path('login/',  method_decorator(csrf_exempt)(views.UserLoginView.as_view()), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('users/', views.UserListView.as_view(), name='alluser'),
]
