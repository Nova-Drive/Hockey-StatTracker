from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, PlayerStats, GoalieStats
from user.models import User
from character.models import Character
from .serializers import PlayerStatsSerializer, GoalieStatsSerializer
import json

def gaa_calc(goals_against, minutes_played):
    assert type(goals_against) == int
    assert type(minutes_played) == int

    return goals_against*60/minutes_played

def get_game(position, game_id):
    if position == 'Goalie':
        return GoalieStats.objects.get(game_id=game_id)
    elif position == 'Player':
        return PlayerStats.objects.get(game_id=game_id)
    else:
        return None
    
def goalie_stats(character, game):
    data = GoalieStatsSerializer(game).data
    data.update({'character': character.name})
    return data

def player_stats(character, game):
    data = PlayerStatsSerializer(game).data
    data.update({'character': character.name})
    return data



#TODO: refactor goalie_maker and player_maker to use serializers
def goalie_maker(data):
    data["character"] = Character.objects.get(id=data['character'])
    return GoalieStats.objects.create(home_team=data['home_team'],
                                away_team=data['away_team'],
                                player_team=data['player_team'],
                                home_score=data['home_score'],
                                away_score=data['away_score'],
                                date=data['date'],
                                season=data['season'],
                                playoff_game=data['playoff_game'],
                                league=data['league'],
                                character=data['character'],
                                shots_against=data['shots_against'],
                                goals_against=data['goals_against'],
                                saves=data['saves'],
                                save_percentage=data['save_percentage'],
                                shutouts=data['shutouts'],
                                minutes_played=data['minutes_played'],
                                goals_against_average=gaa_calc(int(data['goals_against']), int(data['minutes_played'])))

def player_maker(data):
    data["character"] = Character.objects.get(id=data['character'])
    return PlayerStats.objects.create(home_team=data['home_team'],
                                away_team=data['away_team'],
                                player_team=data['player_team'],
                                home_score=data['home_score'],
                                away_score=data['away_score'],
                                date=data['date'],
                                season=data['season'],
                                playoff_game=data['playoff_game'],
                                league=data['league'],
                                character=data['character'],
                                shots=data['shots'],
                                goals=data['goals'],
                                assists=data['assists'],
                                plus_minus=data['plus_minus'],
                                toi=data['toi'],
                                penalty_minutes=data['penalty_minutes'],
                                power_play_goals=data['power_play_goals'],
                                power_play_assists=data['power_play_assists'],
                                short_handed_goals=data['short_handed_goals'],
                                short_handed_assists=data['short_handed_assists'],
                                game_winning_goals=data['game_winning_goals'])

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
            return Response(status=200, data=[goalie_stats(character, game) for game in games])
        
        else:
            games = PlayerStats.objects.filter(character=character)
            return Response(status=200, data=[player_stats(character, game) for game in games])
        

    def post(self, request, username, character):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=character)
        except Character.DoesNotExist:
            return Response(status=404, data={'message': 'Character not found'})
        
        # From this point on, theres a lot of weirdness with characters and data
        # Basically I want the character name in the response, but the serializer wants the character id, and
        # the model wants the character object. So the value of data['character'] changes a lot

        data = request.data.copy().dict()
        data['character'] = character.id
        # print("Character: " + character.name + ", ID : " + str(data['character']))

        if character.position in goalie_abbr:
            serializer = GoalieStatsSerializer(data=data)
            if serializer.is_valid():
                game = goalie_maker(data)
                # print("xyz: {}".format(data))
                game.save()
                data.update({'game_id': '{}'.format(game.game_id)})
                data.update({'message': 'Game created successfully'})
                data.update({'character': character.name})
                # print("abc: {}".format(data))
                data = json.dumps(data)
                return Response(status=201, data=data)
            else:
                print(serializer.errors)
                return Response(status=400, data={'message': 'Invalid data'})

        elif character.position == 'Player':
            serializer = PlayerStatsSerializer(data=data)
            if serializer.is_valid():
                game = player_maker(data)
                game.save()
                data.update({'game_id': '{}'.format(game.game_id)})
                data.update({'message': 'Game created successfully'})
                data.update({'character': character.name})
                # print("zxy: ", data)
                data = json.dumps(data)
                return Response(status=201, data=data)
            else:
                # print(serializer.errors)
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
                game = get_game(character.position, game_id)
            except Game.DoesNotExist:
                return Response(status=404, data={'message': 'Game not found'})
            
            if character.position == 'Goalie':
                return Response(status=200, data=goalie_stats(character, game))
            
            if character.position == 'Player':
                return Response(status=200, data=player_stats(character, game))
        
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

            data = request.data.copy().dict()
            data['character'] = character.id
            data['game_id'] = game_id
            #print("\nData: ", data)
            
            # TODO: Double check the serializers and response data
            if character.position == 'Goalie':
                serializer = GoalieStatsSerializer(game, data=data)
                if serializer.is_valid():
                    serializer.save()
                    #data = serializer.data
                    return Response(status=200, data=data)
                else:
                    return Response(status=400, data={'message': 'Invalid data'})
                
            if character.position == 'Player':
                serializer = PlayerStatsSerializer(game, data=data)
                if serializer.is_valid():
                    serializer.save()
                    #data = serializer.data

                    data.update({'message': 'Game updated successfully'})
                    data.update({'character': character.name})
                    data = json.dumps(data)
                    return Response(status=200, data=data)
                else:
                    print(serializer.errors)
                    return Response(status=400, data={'message': 'Invalid data'})
                
        def delete(self, request, username, character, game_id):
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
            
            game.delete()
            return Response(status=204, data={'message': 'Game deleted successfully'})