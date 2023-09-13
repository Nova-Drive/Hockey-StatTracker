from django.urls import path
from .views import GameView, GamesView

urlpatterns = [
    path('<str:username>/<str:character>/', GamesView.as_view()),   #POST, GET ALL
    path('<str:username>/<str:character>/<str:game_id>', GameView.as_view()), #GET, PUT, DELETE
]