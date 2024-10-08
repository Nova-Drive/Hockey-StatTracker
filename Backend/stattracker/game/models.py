from django.db import models

# Create your models here.

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    home_team = models.CharField(max_length=20)
    away_team = models.CharField(max_length=20)
    player_team = models.CharField(max_length=20)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    date = models.DateField()
    season = models.CharField(max_length=20)
    playoff_game = models.BooleanField()
    league = models.CharField(max_length=20)
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE, null=True)

    class meta:
        abstract = True

class PlayerStats(Game):
    shots = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    plus_minus = models.IntegerField()
    toi = models.IntegerField() #stored in seconds
    penalty_minutes = models.IntegerField()
    power_play_goals = models.IntegerField()
    power_play_assists = models.IntegerField()
    short_handed_goals = models.IntegerField()
    short_handed_assists = models.IntegerField()
    game_winning_goals = models.IntegerField()

class GoalieStats(Game):
    shots_against = models.IntegerField()
    goals_against = models.IntegerField()
    saves = models.IntegerField()
    save_percentage = models.DecimalField(max_digits=4, decimal_places=3)
    shutouts = models.IntegerField()
    minutes_played = models.IntegerField()
    goals_against_average = models.DecimalField(max_digits=4, decimal_places=2)
    
    
    