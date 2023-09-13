from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, PlayerStats, GoalieStats
from user.models import User
from character.models import Character
from .serializers import PlayerStatsSerializer, GoalieStatsSerializer

def gaa_calc(goals_against, minutes_played):
    return goals_against*60/minutes_played

goalie_abbr = ("Goalie", "G", "goalie", "g")


class GamesView(APIView):

    def get(self, response, username, character):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=character)
        except Character.DoesNotExist:
            return Response(status=404, data={'message': 'Character not found'})
        
        if character.position in goalie_abbr:
            games = GoalieStats.objects.filter(character=character)
            return Response(status=200, data=[GoalieStatsSerializer(game).data for game in games])
        
        else:
            games = PlayerStats.objects.filter(character=character)
            return Response(status=200, data=[PlayerStatsSerializer(game).data for game in games])
        

    def post(self, request, username, character):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=character)
        except Character.DoesNotExist:
            return Response(status=404, data={'message': 'Character not found'})
        
        data = request.data.copy()
        data['character'] = character.user.username + character.name
        print(data['character'])

        if character.position == 'Goalie':
            serializer = GoalieStatsSerializer(data=request.data)
            if serializer.is_valid():
                game = GoalieStats(serializer)
                game.save()
                data = {'message': 'Game created successfully'} + game.data
                return Response(status=201, data=data)
            else:
                print(serializer.errors)
                return Response(status=400, data={'message': 'Invalid data'})

        elif character.position == 'Player':
            serializer = PlayerStatsSerializer(data=request.data)
            if serializer.is_valid():
                game = PlayerStats(PlayerStatsSerializer(data=request.data))
                game.save()
                data = {'message': 'Game created successfully'} + game.data
                return Response(status=201, data=data)
            else:
                print(serializer.errors)
                return Response(status=400, data={'message': 'Invalid data'})
            
        else:
            return Response(status=400, data={'message': 'Invalid data'})
        

class GameView(APIView):
    
        def get(self, request, username, character, game_id):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=404, data={'message': 'User not found'})
            
            try:
                character = Character.objects.get(user=user, name=character)
            except Character.DoesNotExist:
                return Response(status=404, data={'message': 'Character not found'})
            
            try:
                game = Game.objects.get(character=character, game_id=game_id)
            except Game.DoesNotExist:
                return Response(status=404, data={'message': 'Game not found'})
            
            #TODO: refactor using serializers
            if character.position == 'Goalie':
                return Response(status=200, data={'game_id':game.game_id, 
                                                'home_team':game.home_team, 
                                                'away_team': game.away_team,
                                                'date':game.date,
                                                'playoff_game':game.playoff_game,
                                                'league':game.league,
                                                'shots_against':game.shots_against,
                                                'goals_against':game.goals_against,
                                                'saves':game.saves,
                                                'save_percentage':game.save_percentage,
                                                'shutouts':game.shutouts,
                                                'minutes_played':game.minutes_played,
                                                'goals_against_average':game.goals_against_average})
            
            if character.position == 'Player':
                return Response(status=200, data={'game_id':game.game_id, 
                                                'home_team':game.home_team, 
                                                'away_team': game.away_team,
                                                'date':game.date,
                                                'playoff_game':game.playoff_game,
                                                'league':game.league,
                                                'shots':game.shots,
                                                'goals':game.goals,
                                                'assists':game.assists,
                                                'plus_minus':game.plus_minus,
                                                'toi':game.toi,
                                                'penalty_minutes':game.penalty_minutes,
                                                'power_play_goals':game.power_play_goals,
                                                'power_play_assists':game.power_play_assists,
                                                'short_handed_goals':game.short_handed_goals,
                                                'short_handed_assists':game.short_handed_assists,
                                                'game_winning_goals':game.game_winning_goals})
        
        def put(self, request, username, character, game_id):
            # don't need to worry about someone manually creating a game with a game_id that doesn't exist
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=404, data={'message': 'User not found'})
            
            try:
                character = Character.objects.get(user=user, name=character)
            except Character.DoesNotExist:
                return Response(status=404, data={'message': 'Character not found'})
            
            try:
                game = Game.objects.get(character=character, game_id=game_id)
            except Game.DoesNotExist:
                return Response(status=404, data={'message': 'Game not found'})
            
            # TODO: Double check the serializers and response data
            if character.position == 'Goalie':
                serializer = GoalieStatsSerializer(game, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200, data={'message': 'Game updated successfully', 'game_id': game.game_id, 'home_team': game.home_team, 'away_team': game.away_team, 'date': game.date})
                else: 
                    return Response(status=400, data={'message': 'Invalid data'})
                
            if character.position == 'Player':
                serializer = PlayerStatsSerializer(game, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200, data={'message': 'Game updated successfully', 'game_id': game.game_id, 'home_team': game.home_team, 'away_team': game.away_team, 'date': game.date})
                else:
                    return Response(status=400, data={'message': 'Invalid data'})
            

            
