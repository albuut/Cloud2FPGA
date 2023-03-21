from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from account.models import User
from games.models import Games
from games.api.serializers import GamesSerializer

@api_view(['GET',])
def all_games(request):
    try:
        game = Games.objects.all()
    except Games.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GamesSerializer(game, many=True)
    return Response(serializer.data)

class ApiGameListView(ListAPIView):
    serializer_class = GamesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(account_id=user_id)
        user_games = user.game.all()
        all_games = Games.objects.all()
        return all_games.difference(user_games).order_by('game_name')