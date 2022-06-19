from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
# Create your views here.

class ClientSignupView(generics.GenericAPIView):
    serializer_class=ClientSignupSerializer
    def post(self, request, *args, **kwargs):

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        client = Client.objects.get(user_id=user.pk)
        serializer=ClientSerializer(client,many=False)
        return Response(
            serializer.data
            #'user':UserSerializer(user, context=self.get_serializer_context()).data,
            #'token':Token.objects.get(user=user).key,
            #'message':'account created successfully'
        )

class DriverSignupView(generics.GenericAPIView):
    serializer_class=DriverSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        driver = Driver.objects.get(user_id=user.pk)
        print(driver)
        serializer=DriverSerializer(driver,many=False)
        return Response(
            serializer.data
            #'user':UserSerializer(user, context=self.get_serializer_context()).data,
            #'token':Token.objects.get(user=user).key,
            #'message':'account created successfully'
        )
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data['user']
        if 'firebaseID' not in request.data:
             return Response({"error":"firebaseID is not definned"
                             
                            }) 
        if 'alt' not in request.data or 'long' not in request.data:
             return Response({"error":"activate GPS ( alt and log are  not definned)"
                             
                            }) 
       
        alt=request.data['alt']
        log=request.data['long']
        point=Point(alt=alt,log=log)
        nbrofPoint=Point.objects.filter(alt=alt,log=log).count()
        if nbrofPoint==0:
            point.save()
        point=Point.objects.get(alt=alt,log=log)
        user.point_actuelle=point
        user.firebaseID=request.data['firebaseID']
        user.is_connected=True
        user.save()
        #token, created=Token.objects.get_or_create(user=user)
        
        if user.typeCompte=='driver':
            driver =Driver.objects.get(user_id=user.id)
            #ser=    DriverSerializer(,many=False)
            return Response({"id":driver.id , 
                            "username":  driver.user.username,
                            "first_name": driver.user.first_name,
                            "last_name":  driver.user.last_name,
                            #"email":      driver.user.email,
                            "typeCompte": driver.user.typeCompte,
                            "firebaseID": driver.user.firebaseID,
                             "log":driver.point_actuelle.log,
                             "alt":driver.point_actuelle.alt,
                            })    
        else:
            client=Client.objects.get(user_id=user.id)
            #ser=    ClientSerializer(client,many=False)
            return Response({
                            "id":client.id , 
                            "username": client.user.username,
                            "first_name": client.user.first_name,
                            "last_name": client.user.last_name,
                            #"email": client.user.email,
                            "typeCompte": client.user.typeCompte,
                            "firebaseID": client.user.firebaseID,
                            "typeclient": client.typeclient,
                            "log":client.point_actuelle.log,
                            "alt":client.point_actuelle.alt,
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
        if not pk.startswith('0'):
            client = Client.objects.get(id=pk)
            #serializer = DriverSerializer(client,many=False)
            return Response({
                            "id":client.id , 
                            "username": client.user.username,
                            "first_name": client.user.first_name,
                            "last_name": client.user.last_name,
                            #"email": client.user.email,
                            "typeCompte": client.user.typeCompte,
                            "firebaseID": client.user.firebaseID,
                             "typeclient": client.typeclient
                            })
        elif  pk.startswith('0') :
            user=User.objects.get(username=pk)
            client = Client.objects.get(user=user.id)
            #serializer = DriverSerializer(client,many=False)
            return Response({
                            "id":client.id , 
                            "username": client.user.username,
                            "first_name": client.user.first_name,
                            "last_name": client.user.last_name,
                            #"email": client.user.email,
                            "typeCompte": client.user.typeCompte,
                            "firebaseID": client.user.firebaseID,
                             "typeclient": client.typeclient
                            })
    except Client.DoesNotExist as err:        
        print(err)
        return Response({'err':' {}'.format(err)})


@api_view(['GET'])
def getClientFav(request,pk):
    
    try:
        #print([field.name for field in Amite._meta.get_fields()] )
        client =Client.objects.get(id=pk)
        amites = Amite.objects.filter(id_client=pk)
        drivers=[]
        for amite in amites:
            drivers.append(amite.id_driver)
        if len(drivers)==0:
            return Response({'drivers':'no drivers yets'})
        serializer = DriverSerializer(drivers,many=True)
        return Response(serializer.data)
    except Client.DoesNotExist as err:  
            return Response({'err':' client do est exist ({})'.format(err)})
    except Amite.DoesNotExist as err:        
        print(err)
        return Response({'err':' {}'.format(err)})

@api_view(['POST','DELETE'])
def addandDeleteClientFav(request):
    id_client=request.data['id_client']
    id_driver=request.data['id_driver']
    try:
            id_client=int(id_client)
            id_driver=int(id_driver)
    except Exception:
            return Response({'err':'id format is not correct(must be integer) '})
    try:
            client=Client.objects.get(id=id_client)

    except Client.DoesNotExist as e:
            return Response({'err':' {}'.format(e)})
    try:
            driver=Driver.objects.get(id=id_driver)

    except Driver.DoesNotExist as e:
            return Response({'err':' {}'.format(e)})

    if request.method == 'POST': 
        
        amite=Amite.objects.filter(id_client=id_client,id_driver=id_driver)
        if amite:
            return Response({'err':' deja ami '})
        else:
            amite=Amite(id_client=client,id_driver=driver)
            amite.save()
        return Response({'succes':'  we add rthis relation:D '})
    elif  request.method == 'DELETE': 
        amite=Amite.objects.filter(id_client=id_client,id_driver=id_driver)
        if not  amite:
            return Response({'err':' ne sont pas des  ami '})
        else:
            amite=Amite.objects.get(id_client=client,id_driver=driver)
            amite.delete()
        return Response({'succes':'  we add rthis relation:D '})
        
@api_view(['GET'])
def getClients(request):
    client = Client.objects.all()

    serializer = ClientSerializer(client,many=True)
    return Response(serializer.data)
 

@api_view(['PUT'])
def activateDriver(request,pk):
    
    try:
            driver = Driver.objects.get(id=pk)
            user=User.objects.get(id=driver.user_id)
            user.is_active=1
            user.save()
            serializer = DriverSerializer(driver,many=False)
            return Response(serializer.data)
    except Driver.DoesNotExist as err:        
        return Response({'err':' {}'.format(err)})


@api_view(['GET'])
def getDrivers(request):
    client = Driver.objects.all()

    serializer = DriverSerializer(client,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def getDriver(request,pk):
    driver = Driver.objects.get(id=pk)

    serializer = DriverSerializer(client,many=False)
    return Response({"id":driver.id , 
                            "username":  driver.user.username,
                            "first_name": driver.user.first_name,
                            "last_name":  driver.user.last_name,
                            #"email":      driver.user.email,
                            "typeCompte": driver.user.typeCompte,
                            "firebaseID": driver.user.firebaseID,
                             
                            })


#--------------------------------------------------
@api_view(['PUT'])
def updatePlacemntDriver(request):
    
    try:
            pk=request.data['id']
            driver = Driver.objects.get(id=pk)
            user=User.objects.get(id=driver.user_id)
            log=request.data['log']
            alt=request.data['alt']
            point=Point(alt=alt,log=log)
            nbrofPoint=Point.objects.filter(alt=alt,log=log).count()
            if nbrofPoint==0:
                point.save()
            point=Point.objects.get(alt=alt,log=log)
            user.point_actuelle=point
        
            user.save()
            #serializer = DriverSerializer(driver,many=False)
            return Response({"id":driver.id , 
                            "username":  driver.user.username,
                            "first_name": driver.user.first_name,
                            "last_name":  driver.user.last_name,
                            #"email":      driver.user.email,
                            "typeCompte": driver.user.typeCompte,
                            "firebaseID": driver.user.firebaseID,
                             "log":driver.user.point_actuelle.log,
                             "alt":driver.user.point_actuelle.alt,
                            })
    except Driver.DoesNotExist as err:        
        return Response({'err':' {}'.format(err)})

@api_view(['PUT'])
def updatePlacemntClient(request):
    
    try:
            pk=request.data['id']
            client = Client.objects.get(id=pk)
            user=User.objects.get(id=client.user_id)
            log=request.data['log']
            alt=request.data['alt']
            point=Point(alt=alt,log=log)
            nbrofPoint=Point.objects.filter(alt=alt,log=log).count()
            if nbrofPoint==0:
                point.save()
            point=Point.objects.get(alt=alt,log=log)
            user.point_actuelle=point
        
            user.save()
            #serializer = DriverSerializer(driver,many=False)
            return Response({
                            "id":client.id , 
                            "username": client.user.username,
                            "first_name": client.user.first_name,
                            "last_name": client.user.last_name,
                            #"email": client.user.email,
                            "typeCompte": client.user.typeCompte,
                            "firebaseID": client.user.firebaseID,
                            "typeclient": client.typeclient,
                            "log":client.user.point_actuelle.log,
                            "alt":client.user.point_actuelle.alt,
                            })
    except Client.DoesNotExist as err:        
        return Response({'err':' {}'.format(err)})
