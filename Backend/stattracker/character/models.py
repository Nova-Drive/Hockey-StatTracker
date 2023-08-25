from django.db import models

# Create your models here.

class Character(models.Model):
    name = models.charField(max_length=20)
    position = models.charField(max_length=20)
    team = models.charField(max_length=20)
