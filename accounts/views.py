
from .models import User
from django.contrib.auth import logout
from django.contrib.auth import  login
from django.contrib.auth import  login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from .models import User
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()








class UserRegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "product/pages-register.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST.get('name', '') 
            return render(request,'product/pages-error-404.html', {"name":name})
        else:
            return render(request,"product/alert.html", {'form': form})












class UserLoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'product/pages-login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Received email: {email}, password: {password}")
    
        username = email 
        backend = 'accounts.authentication.UserPhoneBackend'# if username.isdigit() else 'django.contrib.auth.backends.ModelBackend'
        user = authenticate(request=request, backend=backend, username=username, password=password)
    
        if user and user.is_active:
            login(request, user)
            messages.success(request, 'شما با موفقیت وارد شده‌اید.')
            return render(request, 'product/login_message.html', {"user": user})
        else:
            print("Login failed")
            messages.error(request, 'ورود ناموفق. لطفاً دوباره تلاش کنید.')
            return render(request, 'product/pages-login.html', {"user": user})
        #print(f"Attempting login with email: {email}, password: {password}")
        #user = authenticate(request=request, username=email, password=password)

        #print(f"Authentication result: {user}")

        
            
                
            










class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'product/progres.html', {})



