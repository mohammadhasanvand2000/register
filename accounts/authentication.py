from django.contrib.auth.backends import BaseBackend
from .models import User

class UserPhoneBackend(BaseBackend):
    def authenticate(self, request, backend=None, username=None, password=None, **kwargs):
       
        try:
            if username:
                user = User.objects.get(email=username)
            
                print (user.name)
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
