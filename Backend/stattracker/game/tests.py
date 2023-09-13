from django.test import TestCase
from rest_framework.test import APIClient
from .models import Game, PlayerStats, GoalieStats
from user.models import User
from character.models import Character
from .serializers import PlayerStatsSerializer, GoalieStatsSerializer

# Create your tests here.

player_stats_data = {
    'home_team': 'Edmonton',
    'away_team': 'test2',
    'player_team': 'test',
    'date': '2020-01-01',
    'season': '19-20',
    'playoff_game': False,
    'league': 'NHL',
    'character': 'test2',
    'shots': 2,
    'goals': 1,
    'assists': 2,
    'plus_minus': 1,
    'toi': 1200,
    'penalty_minutes': 2,
    'power_play_goals': 1,
    'power_play_assists': 1,
    'short_handed_goals': 0,
    'short_handed_assists': 1,
    'game_winning_goals': 1
}

goalie_stats_data = {
    'home_team': 'Toronto',
    'away_team': 'test2',
    'player_team': 'test',
    'date': '2020-01-01',
    'season': '19-20',
    'playoff_game': False,
    'league': 'NHL',
    'character': 'test',
    'shots_against': 2,
    'goals_against': 1,
    'saves': 1,
    'save_percentage': 0.5,
    'shutouts': 1,
    'minutes_played': 1200,
    'goals_against_average': 1.0
}

def data_to_player_game(data, character):
    return PlayerStats.objects.create(home_team=data['home_team'],
                                away_team=data['away_team'],
                                player_team=data['player_team'],
                                date=data['date'],
                                season=data['season'],
                                playoff_game=data['playoff_game'],
                                league=data['league'],
                                character=character,
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
                                game_winning_goals=data['game_winning_goals']
    )

def data_to_goalie_game(data, character):
    return GoalieStats.objects.create(home_team=data['home_team'],
                                away_team=data['away_team'],
                                player_team=data['player_team'],
                                date=data['date'],
                                season=data['season'],
                                playoff_game=data['playoff_game'],
                                league=data['league'],
                                character=character,
                                shots_against=data['shots_against'],
                                goals_against=data['goals_against'],
                                saves=data['saves'],
                                save_percentage=data['saves']/data['shots_against'],
                                shutouts=data['shutouts'],
                                minutes_played=data['minutes_played'],
                                goals_against_average=data['goals_against_average']
                                )




class GameTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="test", email="test@gmail.com")

        # Player
        self.character = Character.objects.create(name="test", position="Player", team="test", user=self.user)
        #Goalie
        self.character2 = Character.objects.create(name="test2", position="Goalie", team="test", user=self.user)
        # empty character
        self.character3 = Character.objects.create(name="test3", position="Player", team="test", user=self.user)

        # turn the data into a game 
        self.player_game = data_to_player_game(player_stats_data, self.character)
        self.goalie_game = data_to_goalie_game(goalie_stats_data, self.character2)


    def test_get_games(self):
        # Refactor to use response for character instead of test character object
        response = self.client.get('/test/test/')
        self.assertEqual(PlayerStats.objects.filter(character=self.character).count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], PlayerStatsSerializer(self.player_game).data)

        response = self.client.get('/test/test2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], GoalieStatsSerializer(self.goalie_game).data)

    def test_get_games_not_found(self):
        response = self.client.get('/test/test3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_post_game(self):
        #TODO: add more testing to make sure games actually show up

        # create the game and make sure it shows up under broad GET
        response = self.client.post('/test/test/', player_stats_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, PlayerStatsSerializer(PlayerStats.objects.filter(character=self.character).last()).data)

        # test that the game is actually created
        response = self.client.get('/test/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1], PlayerStatsSerializer(PlayerStats.objects.filter(character=self.character).last()).data)

        # now the same thing for the goalie game
        response = self.client.post('/test/test', goalie_stats_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, GoalieStatsSerializer(GoalieStats.objects.filter(character=self.character).last()).data)

        
        response = self.client.get('/test/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[2], GoalieStatsSerializer(GoalieStats.objects.filter(character=self.character).last()).data)
        
