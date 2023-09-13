from .models import Character
from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

class CharactersView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        characters = Character.objects.filter(user=user)
        return Response(status=200,
                    data=[{'name': character.get_name(),
                            'position': character.get_position(),
                            'team': character.get_team() 
                    } for character in characters])
    

    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=request.data['name'])
        except Character.DoesNotExist:
            pass
        else:
            return Response(status=400, data={'message': 'Character already exists'})
        
        character = Character(name=request.data['name'], position=request.data['position'], team=request.data['team'], user=user)
        character.save()
        return Response(status=201, data={'message': 'Character created successfully', 'name': character.get_name(), 'position': character.get_position(), 'team': character.get_team()})
    
class CharacterView(APIView):

    def get(self, request, username, character_name):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=character_name)
        except Character.DoesNotExist:
            return Response(status=404, data={'message': 'Character not found'})
        
        return Response(status=200, data={'name': character.get_name(), 'position': character.get_position(), 'team': character.get_team()})
    
    def put(self, request, username, character_name):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=character_name)
        except Character.DoesNotExist:
            return Response(status=404, data={'message': 'Character not found'})
        
        try:
            character2 = Character.objects.get(user=user, name=request.data['name'])
        except Character.DoesNotExist:
            pass
        else:
            return Response(status=400, data={'message': 'Name already exists'})
        
        character.set_name(request.data['name'])
        character.set_position(request.data['position'])
        character.set_team(request.data['team'])
        character.save()
        return Response(status=200, data={'message': 'Character updated successfully', 'name': character.get_name(), 'position': character.get_position(), 'team': character.get_team()})
    
    def delete(self, request, username, character_name):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        try:
            character = Character.objects.get(user=user, name=character_name)
        except Character.DoesNotExist:
            return Response(status=404, data={'message': 'Character not found'})
        
        character.delete()
        return Response(status=204)