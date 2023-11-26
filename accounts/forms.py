from django import forms
from .models import User
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields ="__all__"




class UserLoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email:
            raise forms.ValidationError("باید حداقل یکی از «ایمیل» را وارد کنید.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("کاربر با این ایمیل وجود ندارد.")

        if not user.check_password(password):
            raise forms.ValidationError("پسورد نامعتبر. لطفا دوباره تلاش کنید.")

        if not user.is_active:
            raise forms.ValidationError("حساب کاربری غیرفعال است")

        return cleaned_data