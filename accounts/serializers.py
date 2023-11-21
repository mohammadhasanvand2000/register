from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, login
from .validators import validate_iranian_phoneNumber
from django.shortcuts import get_object_or_404


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"




class UserLoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=False)
   
    password = serializers.CharField()

    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("باید حداقل یکی از «ایمیل» را وارد کنید.")

        user = get_object_or_404(User, email=email)
        
        if not user.check_password(password):
            print (password)
            raise serializers.ValidationError("پسورد نامعتبر. لطفا دوباره تلاش کنید.")

        if not user.is_active:
            raise serializers.ValidationError("حساب کاربری غیرفعال است")

        data['user'] = user
        return data
