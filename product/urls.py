
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  index ,UploadAPIView,UploadAndEmailAPIView,SelectAPIView,SendEmailAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#router = DefaultRouter()

#router.register('', ProductViewSet)

urlpatterns = [
   path('', index, name='index'),
   path('upload/', method_decorator(csrf_exempt)(UploadAPIView.as_view()), name='upload'),
   path('upload-csv/', UploadAndEmailAPIView.as_view(), name='upload_csv_api'),
   path('select/', method_decorator(csrf_exempt)(SelectAPIView.as_view()), name='select'),
   path('send/', method_decorator(csrf_exempt)(SendEmailAPIView.as_view()), name='send'),
]