from django.urls import path
from .views import UserView

urlpatterns = [
    path('', UserView.as_view()),   #POST
    path('<str:username>', UserView.as_view()), #GET, PUT, DELETE
]