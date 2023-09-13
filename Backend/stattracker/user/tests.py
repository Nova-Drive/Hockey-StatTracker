from django.test import TestCase
from rest_framework.test import APIClient
from .models import User
# Create your tests here.

#create api client tests
class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="test", email="test@gmail.com")
        self.user2 = User.objects.create(username="test2", email="test2@gmail.com")

    
    """ def test_get_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], self.user.username)
        self.assertEqual(response.data[0]['email'], self.user.email)
        self.assertEqual(response.data[1]['username'], self.user2.username)
        self.assertEqual(response.data[1]['email'], self.user2.email)
 """
    def test_get_user(self):
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_user_not_found(self):
        response = self.client.get('/test3')
        self.assertEqual(response.status_code, 404)

    def test_post_user(self):
        response = self.client.post('/', {'username': 'test3', 'email': 'test3@gmail.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'test3')
        self.assertEqual(response.data['email'], 'test3@gmail.com')
        assert User.objects.filter(username='test3').exists()
        self.assertEqual(User.objects.get(username='test3').username, response.data['username'])
        self.assertEqual(User.objects.get(username='test3').email, response.data['email'])


    def test_post_user_already_exists(self):
        response = self.client.post('/', {'username': 'test', 'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 400)

    def test_put_user(self):
        response = self.client.put('/test', {'username': 'test3', 'email': 'test3@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'test3')
        self.assertEqual(response.data['email'], 'test3@gmail.com')

    def test_put_user_not_found(self):
        response = self.client.put('/test4', {'username': 'test3', 'email': 'test3@gmail.com'})
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        response = self.client.delete('/test')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 404)

    def test_delete_user_not_found(self):
        response = self.client.delete('/test4')
        self.assertEqual(response.status_code, 404)
