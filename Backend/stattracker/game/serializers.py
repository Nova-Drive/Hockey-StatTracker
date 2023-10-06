from rest_framework import serializers
from .models import PlayerStats, GoalieStats

class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStats
        fields = '__all__'
        #exclude = ['game_id']

class GoalieStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalieStats
        fields = '__all__'
        #exclude = ['game_id']

