from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authentication import TokenAuthentication

from account.api.serializers import RegistrationSerializer, UserGameSerializer
from games.api.serializers import GamesSerializer
from rest_framework.authtoken.models import Token


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import FileResponse


from account.models import User
from account.api.serializers import UserGameSerializer,UserSyncSerializer, UserStorageInfo
from django.core.files.storage import default_storage




# Create your views here.
@api_view(['POST',])
@permission_classes((AllowAny,))
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

class UserGameApiView(ListAPIView):
    serializer_class = GamesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(account_id=user_id)
        return user.game.all()

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

class UserStorageInfoView(RetrieveAPIView):
    serializer_class = UserStorageInfo
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        user = User.objects.get(account_id=user_id)
        return user
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