from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework import generics

from .models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserRegistrationSerializer, UserLoginSerializer,UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.renderers import TemplateHTMLRenderer

from django.views.decorators.csrf import csrf_exempt



from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer



class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class =UserRegistrationSerializer
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        
        return render(request, 'product/pages-register.html')

    def post(self, request):
       
        #name = request.data.get('name')
        #email = request.data.get('email')
        #username=request.data.get('username')
        #phoneNumber = request.data.get('phoneNumber')
        #password = request.data.get('password')
        print(request.data)  
       
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
           
            return render(request,'product/pages-error-404.html',{})
        else:
           
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class=UserLoginSerializer
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request):
        
        return render(request, 'product/pages-login.html')
    def post(self, request):
        
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        
        password = serializer.validated_data.get('password')
        username=email 
        backend = 'accounts.authentication.UserPhoneBackend'# if username.isdigit() else 'django.contrib.auth.backends.ModelBackend'
        
        
        user = authenticate(request=request, backend=backend, username= email , password=password)
        print(email)
        if user is not None:
            login(request, user)
            
            return HttpResponseRedirect('/')
            
        else:
            return Response({"message": "یوزر وجود ندارد"}, status=status.HTTP_401_UNAUTHORIZED)






class UserLogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": " شما با موفقیت خارج شدید ."}, status=status.HTTP_200_OK)







class UserListView(generics.ListAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer