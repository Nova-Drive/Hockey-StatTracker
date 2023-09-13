from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response

class UserView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        return Response(status=200, data={'username': user.get_username(), 'email': user.get_email()})
    
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            pass
        else:
            return Response(status=400, data={'message': 'User already exists'})

        user = User(username=request.data['username'], email=request.data['email'])
        user.save()
        return Response(status=201, data={'message': 'User created successfully', 'username': user.get_username(), 'email': user.get_email()})
    
    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})

        user.set_username(request.data['username'])
        user.set_email(request.data['email'])
        user.save()
        return Response(status=200, data={'message': 'User updated successfully', 'username': user.get_username(), 'email': user.get_email()})
    
    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=404, data={'message': 'User not found'})
        
        user.delete()
        return Response(status=204)
    


