# views.py
from django.views.decorators.csrf import csrf_exempt
from .models import Upload
from django.shortcuts import render,HttpResponseRedirect
from rest_framework import  generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UploadSerializer
from django.utils.decorators import method_decorator
from .Util import Util
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PersonSerializer,PersonSelectedSerializer  
from django.shortcuts import render
from .models import Upload ,Person
from .serializers import PersonSerializer
import csv
import re

def index(request):
    return render(request,"product\index.html",{})



class UploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'product/forms-elements.html')

    def post(self, request):
        serializer = UploadSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return render(request,"product/alert.html",{})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








email_regex_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_number_regex_pattern = r'^09\d{9}$'
name_regex_pattern = r'^[a-zA-Z\s]{6,}$'
national_code_regex_pattern = r'^\d{10}$'



class UploadAndEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer

    def get(self, request):
        try:
       
            upload_instance = Upload.objects.all()
            
            persons_created = []
            for i in upload_instance.filter(owner__name=request.user.name):
                with open(i.file.path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    persons_data = list(csv_reader)
                    
                    values_list = [record.values() for record in persons_data]
                    data_list = [list(item) for item in values_list]
                    
                    for record in data_list:
                        for value in record:
        
                            values = value.split(',')
                            
                     
                            
                            result_json = {}

                            for index, value in enumerate(values):
                                if re.match(email_regex_pattern, value):
                                    result_json['email'] = value
                                elif re.match(phone_number_regex_pattern, value):
                                    result_json['phoneNumber'] = value
                                elif re.match(name_regex_pattern, value):
                                    result_json['name'] = value
                                elif re.match(national_code_regex_pattern, value):
                                    result_json['national_code'] = value

                            print(result_json)
                    
                       
                            serializer = PersonSerializer(data=result_json)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()
                            persons_created.append(serializer.data)
                            
            
            return render(request,"product\split.html",{})

        except Upload.DoesNotExist:
            return Response({'detail': 'مورد مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
        

        


class SelectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    template_name = "product/tables-data.html"
   
    def get(self, request):
        person = Person.objects.all()
       
        return render(request, self.template_name, {"person": person})
    @method_decorator(csrf_exempt)
    def post(self, request):
        print(request.data)

        selected_person_ids = request.data.getlist('selected_person_ids', [])
        count_updated_rows = 0  

        for i in selected_person_ids:
        
            updated_rows = Person.objects.filter(id=i).update(selected=True)

        
            count_updated_rows += updated_rows

            if count_updated_rows > 0:
        
                print("At least one row is updated.")
            else:
        
                print("No row is updated.")

        return Response({'message': 'Data received successfully'})





class SendEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        
        upload_instance = Upload.objects.all()
        email_list = []  
        
        for i in upload_instance.filter(owner__name=request.user.name):
            message = i.message
        person = Person.objects.filter(selected=True)
        print(person)
        for p in person:
            print(p.email)
            email_list.append(p.email)  
            
        
            self.send_email(email_list, message)
            
            
        return render(request,"product/progres.html",{})
            
       

    def send_email(self, email_list, message):
  
        for email in email_list:
            data = {'email_body': message, 'to_email': email, 'email_subject': ('ثبت نام شدید ')} 
            Util.send_email(data)


          