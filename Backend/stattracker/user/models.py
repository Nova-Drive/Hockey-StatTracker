from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.CharField(max_length=50)

    
    