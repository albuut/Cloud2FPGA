from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import FileResponse


from account.models import User
from games.models import Games
from account.api.serializers import UserGameSerializer,UserSyncSerializer,GameSerializer
from django.core.files.storage import default_storage




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



@api_view(['GET',])
def userGameAPI(request,id=0):
    if request.method=='GET':
        #If the payload from the script does no match then it blows up the code. fix later on
        user_id = request.GET['value']
        
        #Checks to see if the value is an actual user
        #need to make sure its length is 26 characters. if its shorter or longer the function blows up
        users = User.objects.all().filter(account_id=user_id)
        user_serializer = UserGameSerializer(users,many=True)
        data = user_serializer.data
        

        #using FileResponse
        #file = open(data[0]['game'][1]['rma_file'],'rb')
        #response = FileResponse(file)

        ''' 
        --data-- returns the user of the specific user_id
        --data[0]['game']-- returns the list of games to that user
        --data[0]['game'][1]['rma_file']-- returns the file path to the rma file
        #'''

        return JsonResponse(data[0]['game'], safe=False)
        #return JsonResponse(data[0]['game'][1]['rma_file'], safe=False)


@csrf_exempt
def UserSyncAPI(request,id=0):
    if request.method=='GET':
        # #If the payload from the script does no match then it blows up the code. fix later on
        user_id = request.GET['value']
        
        #Checks to see if the value is an actual user
        #need to make sure its length is 26 characters. if its shorter or longer the function blows up
        users = User.objects.all().filter(account_id=user_id)
        user_serializer = UserSyncSerializer(users,many=True)
        data = user_serializer.data    
        return JsonResponse(data, safe=False)
    
    elif request.method=='PUT':
        user_data = JSONParser().parse((request))

        user=User.objects.get(account_id=user_data['value'])
        user_serializer = UserSyncSerializer(user,data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Update Successfully",safe=False)
        return JsonResponse("Failed",safe=False)

@csrf_exempt
def UpdateUserGameAPI(request,id=0):
    if request.method=='PUT':
        user_data = JSONParser().parse((request))

        user=User.objects.get(account_id=user_data['value'])
        user_serializer = UserSyncSerializer(user,data=user_data)
        data = user_serializer.data
        # if user_serializer.is_valid():
        #     user_serializer.save()
        #     return JsonResponse("Update Successfully",safe=False)
        return JsonResponse(data,safe=False)


class ChildCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        parent_id = request.data.get('acount_id')
        game_name = request.data.get('game_name')


        parent = User.objects.filter(account_id=parent_id).first()

        if not parent:
            return Response({'acount_id': 'Invalid parent id'}, status=status.HTTP_400_BAD_REQUEST)

        child = Games.objects.get(game_name=game_name)
        parent.game.add(child)

        serializer = self.get_serializer(child)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)