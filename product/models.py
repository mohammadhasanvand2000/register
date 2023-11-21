from django.db import models
from accounts.models import User 


class Upload (models.Model):
    owner        = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email_ow     = models.EmailField()
    password_em  = models.CharField(max_length=50)
    message      = models.TextField()
    file         = models.FileField(upload_to='csv_files/')
    ceeate_at    = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        owner_name = self.owner.name if self.owner.name else  "No Owner"
        return f"{owner_name} - {self.email_ow}"
    





class Person(models.Model):
    
    name            = models.CharField(max_length=255,null=True, blank=True)
    phoneNumber     = models.CharField(max_length=15 ,null=True, blank=True)
    national_code   = models.CharField(max_length=10)
    email           = models.EmailField()
    selected        = models.BooleanField(default=False ,null=True,blank=True)

    def __str__(self):
        name = self.name if self.name else "No name"
        return f"{name} - {self.phoneNumber} - {self.national_code} - {self.email}-{self.selected}"