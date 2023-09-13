from django.test import TestCase
from rest_framework.test import APIClient
from user.models import User
from .models import Character

class CharacterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="test", email="email")
        self.user2 = User.objects.create(username="test2", email="email2")
        self.character = Character.objects.create(name="name", position="position", team="team", user=self.user)
        self.character2 = Character.objects.create(name="name2", position="position2", team="team2", user=self.user)

    def test_get_characters(self):
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.character.name)
        self.assertEqual(response.data[0]['position'], self.character.position)
        self.assertEqual(response.data[0]['team'], self.character.team)
        self.assertEqual(response.data[1]['name'], self.character2.name)
        self.assertEqual(response.data[1]['position'], self.character2.position)
        self.assertEqual(response.data[1]['team'], self.character2.team)

    def test_get_characters_not_found(self):
        response = self.client.get('/test2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_post_character(self):
        response = self.client.post('/test/', {'name': 'name3', 'position': 'position3', 'team': 'team3'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'name3')
        self.assertEqual(response.data['position'], 'position3')
        self.assertEqual(response.data['team'], 'team3')
        assert Character.objects.filter(name='name3').exists()
        self.assertEqual(Character.objects.get(name='name3').name, response.data['name'])
        self.assertEqual(Character.objects.get(name='name3').position, response.data['position'])
        self.assertEqual(Character.objects.get(name='name3').team, response.data['team'])
        self.assertEqual(len(self.client.get('/test/').data), 3)

    def test_post_character_already_exists(self):
        response = self.client.post('/test/', {'name': 'name', 'position': 'position', 'team': 'team'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/test/', {'name': 'name', 'position': 'positionx', 'team': 'teamy'})
        self.assertEqual(response.status_code, 400)

    def test_put_character(self):
        response = self.client.put('/test/name', {'name': 'name3', 'position': 'position3', 'team': 'team3'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'name3')
        self.assertEqual(response.data['position'], 'position3')
        self.assertEqual(response.data['team'], 'team3')
        character = Character.objects.get(name='name3')
        self.assertEqual(character.name, response.data['name'])
        self.assertEqual(character.position, response.data['position'])
        self.assertEqual(character.team, response.data['team'])

    def test_put_character_not_found(self):
        response = self.client.put('/test/name3', {'name': 'name3', 'position': 'position3', 'team': 'team3'})
        self.assertEqual(response.status_code, 404)

    def test_delete_character(self):
        response = self.client.delete('/test/name')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        try:
            character = Character.objects.get(name='name')
        except Character.DoesNotExist:
            pass
        else:
            self.fail()

    def test_delete_character_not_found(self):
        response = self.client.delete('/test/name3')
        self.assertEqual(response.status_code, 404)

    def test_get_character(self):
        response = self.client.get('/test/name')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.character.name)
        self.assertEqual(response.data['position'], self.character.position)
        self.assertEqual(response.data['team'], self.character.team)

    def test_get_character_not_found(self):
        response = self.client.get('/test/name3')
        self.assertEqual(response.status_code, 404)


