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
        #print(driver)
        #serializer=DriverSerializer(driver,many=False)
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
        #to remove
        #if 'alt' not in request.data or 'log' not in request.data:
        #     return Response({"error":"activate GPS ( alt and log are  not definned)"
         #                    }) 
       
        #alt=request.data['alt']
        #log=request.data['log']
        #point=Point(alt=alt,log=log)
        #nbrofPoint=Point.objects.filter(alt=alt,log=log).count()
        #if nbrofPoint==0:
        #    point.save()
        #point=Point.objects.get(alt=alt,log=log)
        #user.point_actuelle=point
        user.firebaseID=request.data['firebaseID']
        user.is_connected=True
        user.save()
        #token, created=Token.objects.get_or_create(user=user)
        
        if user.typeCompte=='driver':
            driver =Driver.objects.get(user_id=user.id)
            #ser=    DriverSerializer(,many=False)
            return Response(driverTodict(driver))    
        else:
            client=Client.objects.get(user_id=user.id)
            #ser=    ClientSerializer(client,many=False)
            return Response(clientTodict(client))           

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
            return Response(clientTodict(client))
        elif  pk.startswith('0') :
            user=User.objects.get(username=pk)
            client = Client.objects.get(user=user.id)
            #serializer = DriverSerializer(client,many=False)
            return Response(clientTodict(client))
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
 

@api_view(['POST'])
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

    serializer = DriverSerializer(driver,many=False)
    return Response(driverTodict(driver))

#-----------------------------------
@api_view(['GET','POST'])
def getVoiture(request,driver):
    #category=request.data['category']
    #driver=request.data['driver']

    voitures=Voiture.objects.filter(id_driver=driver)
    serializer=VoitureSerializer(voitures,many=True)
    return Response(serializer.data)
#--------------------------------------------------
@api_view(['POST'])
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
            driver=Driver.objects.get(user_id=user.id)
            #serializer = DriverSerializer(driver,many=False)
            return Response(driverTodict(driver))
    except Driver.DoesNotExist as err:        
        return Response({'err':' {}'.format(err)})

@api_view(['POST'])
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
            client=Client.objects.get(user_id=user.id)
            #serializer = DriverSerializer(driver,many=False)
            return Response(clientTodict(client))
    except Client.DoesNotExist as err:        
        return Response({'err':' {}'.format(err)})

@api_view(['GET','POST'])
def getNearsetDriver(request,nbr=20):
    #pk=request.data['id']
    #client = Client.objects.get(id=pk)
    #user=User.objects.get(id=client.user_id)
    #if 'category' not in request.data:
    #    return Response({"category":"category is missing"})
    category=request.data['category']
    if "nbr" in request.data:
        nbr=request.data['nbr']

    #point=Point.objects.get(la=user.point_actuelle)
    #The location of your user.
    lat, lng =request.data['alt_dep'],request.data['log_dep'] #user.point_actuelle.alt,user.point_actuelle.log,
    lat=float(lat)
    lng=float(lng)

    distanceVoulu=0.5
    if "rayon" in request.data:
        distanceVoulu=float(request.data['rayon'])//111
    min_lat = lat - distanceVoulu # You have to calculate this offsets based on the user location.
    max_lat = lat + distanceVoulu # Because the distance of one degree varies over the planet.
    min_log = lng - distanceVoulu
    max_log = lng + distanceVoulu    
    voitures = Voiture.objects.filter(
            occupe=True,
            id_cat=Category.objects.get(id=category),
            id_driver__user__is_connected=1,
            id_driver__user__typeCompte="driver",
            id_driver__user__point_actuelle__alt__gt=min_lat,
            id_driver__user__point_actuelle__alt__lt=max_lat, 
            id_driver__user__point_actuelle__log__gt=min_log, 
            id_driver__user__point_actuelle__log__lt=max_log,
    )
    #print(voitures.query)
    results = []
    #https://stackoverflow.com/questions/17903883/using-geopositionfield-to-find-closest-database-entries
    #print(users.query)
    from geopy import distance  
    results = []
    for voiture in voitures:
        d = distance.distance((lat, lng), (voiture.id_driver.user.point_actuelle.alt, voiture.id_driver.user.point_actuelle.log))
        results.append( {'distance':d, 'voiture':voiture.id })
        results = sorted(results, key=lambda k: k['distance'])
    results = results[:nbr]
    print(results)
    results=[r['voiture'] for r in results]
    #drivers=[Driver.objects.get()]
    #users=UserSerializer(results,many=True)
    if len(results)==0:
        return Response({"no voiture":"no voiture availbe"})
    #driver=Driver.objects.filter(user_id__in=results)
    voiture=Voiture.objects.get(id=results[0])
    
    #return Response({"dirver":driver.id})
    #driver=Driver.objects.get(id=voiture.id_driver)
    #driver=DriverSerializer(driver,many=True)
    #return Response(driver.data)

    dictOutput=driverTodict(voiture.id_driver)
    dictOutput['id_voiture']=voiture.id
    try:
        dictOutput['marque']=voiture.id_model.model_name+"( {})".format(voiture.id_model.id_marque.marque_name)
    except :
         dictOutput['marque']="marque n'est pas defini encore"
    dictOutput['category']=voiture.id_cat.cat_name
    dictOutput['alt']=voiture.id_driver.user.point_actuelle.alt
    dictOutput['log']=voiture.id_driver.user.point_actuelle.log

    
    return Response(dictOutput)
#---------------------------------
@api_view(['GET'])
def getCategory(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def chooseVoiture(request):
    #category=request.data['category']
    driver=request.data['driver']
    try:
        driver=Driver.objects.get(id=driver)

    except Driver.DoesNotExist as e:
        return Response({"err":"driver donet exist"})

    
    voiture=request.data['voiture']
    try:
    
        Voiture.objects.get(id=voiture,id_driver=driver)
    except Voiture.DoesNotExist as e:

        return Response({"err":"driver donet own this car or car donest exist"})
    voitures=Voiture.objects.filter(id_driver=driver).update(occupe=False)

    Voiture.objects.filter(id=voiture,id_driver=driver).update(occupe=True)
    voiture = Voiture.objects.get(id=voiture,id_driver=driver)
    serializer=VoitureSerializer(voiture,many=False)
    return Response(serializer.data)



@api_view(['POST'])
def addVoiture(request):
    #category=request.data['category']
    matrciule=request.data['matrciule']
    category=request.data['category']
    id_driver=request.data['driver']
    try:
        category=Category.objects.get(id=category)
    except Category.DoesNotExist as e:
        return Response({"err":"category nexit pas "})
    try:
        id_driver=Driver.objects.get(id=id_driver)
    except Driver.DoesNotExist as e:
        return Response({"err":"Driver nexit pas "})
    
    voiture=Voiture(matrciule=matrciule,id_cat=category,id_driver=id_driver)
    voiture.save()
    #voitures=Voiture.objects.filter(id_driver=driver)
    serializer=VoitureSerializer(voiture,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createCoursa(request):
    client=request.data['client']
    voiture=request.data['voiture']
    alt_dep=request.data['alt_dep']
    log_dep=request.data['log_dep']

    alt_arr=request.data['alt_arr']
    log_arr=request.data['log_arr']
    try:
        client=Client.objects.get(id=client)
    except Client.DoesNotExist as e:
        return Response({"err":"Client n'exit pas "})
    
    try:
        voiture=Voiture.objects.get(id=voiture)
    except Voiture.DoesNotExist as e:
        return Response({"err":"Voiture nexit pas "})
    
    point_dep=Point(alt=alt_dep,log=log_dep)
    nbrofPoint=Point.objects.filter(alt=alt_dep,log=log_dep).count()
    if nbrofPoint==0:
        point_dep.save()
    depart=Point.objects.get(alt=alt_dep,log=log_dep)

    point_arr=Point(alt=alt_arr,log=log_arr)
    nbrofPoint=Point.objects.filter(alt=alt_arr,log=log_arr).count()
    if nbrofPoint==0:
        point_arr.save()
    arrive=Point.objects.get(alt=alt_arr,log=log_arr)

    coursa=Coursa(client=client,voiture=voiture,depart=depart,arrive=arrive)
    coursa.save()
  
    serializer=CoursaSerializer(coursa,many=False)
    return Response(coursaCreationTodict(coursa))
@api_view(['POST'])
def endCoursa(request):
    coursa=request.data['id']
    try :
        coursa=Coursa.objects.get(id=coursa)
    except Coursa.DoesNotExist as e:
        return Response({"err":"Coursa nexit pas "})
    import datetime
    coursa.date_arrive=datetime.datetime.now()
    coursa.save()
    return Response(coursaCreationTodict(coursa,finished=True))