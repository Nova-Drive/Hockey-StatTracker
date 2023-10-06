from django.db import models

# Create your models here.

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    team = models.CharField(max_length=20)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    def get_name(self):
        return self.name
    
    def get_position(self):
        return self.position
    
    def get_team(self):
        return self.team
    
    def set_name(self, name):
        self.name = name

    def set_position(self, position):
        self.position = position

    def set_team(self, team):
        self.team = team
    
