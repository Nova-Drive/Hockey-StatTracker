from django.urls import path
from .views import CharacterView, CharactersView

urlpatterns = [
    path('<str:username>/', CharactersView.as_view()),   #POST, GET ALL
    path('<str:username>/<str:character_name>', CharacterView.as_view()), #GET, PUT, DELETE
]