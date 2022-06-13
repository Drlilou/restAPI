from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Client,User
# Create your views here.

class ClientSignupView(generics.GenericAPIView):
    serializer_class=ClientSignupSerializer
    def post(self, request, *args, **kwargs):

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            #"token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })

class DriverSignupView(generics.GenericAPIView):
    serializer_class=DriverSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            #"token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
       
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data['user']
        
        user.firebaseID=request.data['firebaseID']
        user.is_connected=True
        user.save()
        #token, created=Token.objects.get_or_create(user=user)
        print(user)
        return Response({
            #'token':token.key,
            'user_id':user.pk,
            'typeCompte':user.typeCompte,
            'connection':user.is_connected,
            'firebaseID':user.firebaseID

        })

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        serializer=self.serializer_class(data=request.data, context={'request':request})
       
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data['user']
        
        user.firebaseID=''
        user.is_connected=False
        user.save()
        
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getClient(request,pk):
    
    try:
        if not pk.startswith("0"):
            client = Client.objects.get(id=pk)
            serializer = ClientSerializer(client,many=False)
            return Response(serializer.data)
        elif  pk.startswith("0") :
            user=User.objects.get(username=pk)
            client = Client.objects.get(user=user.id)
            serializer = ClientSerializer(client,many=False)
            return Response(serializer.data)
    except Client.DoesNotExist as err:        
        print(err)
        return Response({"err":" {}".format(err)})
@api_view(['GET'])
def getClients(request):
    client = Client.objects.all()

    serializer = ClientSerializer(client,many=True)
    return Response(serializer.data)
    