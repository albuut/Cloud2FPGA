from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import Games, User

from account.api.serializers import RegistrationSerializer,GameSerializer,UserGameSerializer
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered user"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

class UserGameViewSet(viewsets.ModelViewSet):
    serializer_class = UserGameSerializer

    def get_queryset(self):
        usergameinfo = User.objects.all()
        return usergameinfo

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        gameinfo = Games.objects.all()
        return gameinfo