from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username
    
    def get_email(self):
        return self.email
    
    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email
    