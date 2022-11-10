from django.db import models

# Create your models here.

class ClientAPI(models.Model):
    status = models.CharField(max_length=100)
    inputvalues = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
