from rest_framework import serializers

from .models import *


# signup login logout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    typeuser_name = serializers.RelatedField(source='typeUser', read_only=True)

    class Meta:
        model=Client
        fields = '__all__'
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(
            username=user_data['username'],email=user_data['email'], password=user_data['password'])
        user_instance.save()
        
        staff_instance = Client.objects.create(
            **validated_data, user=user_instance)
        staff_instance.save()
        return staff_instance

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model=Driver
        fields = ['id','user']#,'user']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(
            username=user_data['username'],email=user_data['email'], password=user_data['password'])
        user_instance.save()
        
        staff_instance = Driver.objects.create(
            **validated_data, user=user_instance)
        staff_instance.save()
        return staff_instance

class AmiteSerializer(serializers.ModelSerializer):
    #clientSerializer=ClientSerializer(read_only=True)
    driverSerializer=DriverSerializer(read_only=True)
    class Meta:
        model=Amite
        fields='__all__'#['driverSerializer',]

    
class ClientSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    typeclient=serializers.CharField(style={'input_type':'select'}, write_only=True)
    class Meta:
        model=User
        fields=['tlf','typeclient','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['tlf'],
            email=   self.validated_data['tlf'],
            tlf  = self.validated_data['tlf'],
            #typeclient=self.validated_data('')
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        typeclient=self.validated_data['typeclient']
        if password !=password2:
            raise serializers.ValidationError({'error':'password do not match'})
        if typeclient not in ['pro','simple']:
            raise serializers.ValidationError({"error":"wrong client type, choose wisely"})
        user.set_password(password)
        user.typeCompte='client'
        user.save()
        Client.objects.create(user=user,typeclient=typeclient)
        return user
class DriverSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model=User
        fields=['tlf','password', 'password2',]
        extra_kwargs={
            'password':{'write_only':True}
        }
    

    def save(self, **kwargs):
        user=User(
            username=self.validated_data['tlf'],
            email=self.validated_data['tlf'],
            tlf=self.validated_data['tlf']
            , is_active=0

        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({'error':'password do not match'})
        user.set_password(password)
        user.typeCompte='driver'
        user.save()
        Driver.objects.create(user=user)
        
        return user
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Voiture
        fields='__all__'

class CoursaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coursa
        fields='__all__'


def driversTodict(drivers):
    return set([driverTodict(driver) for driver in drivers])
def driverTodict(driver):
    return {                "id":driver.id , 
                            "username":  driver.user.username,
                            "first_name": driver.user.first_name,
                            "last_name":  driver.user.last_name,
                            #"email":      driver.user.email,
                            "typeCompte": driver.user.typeCompte,
                            "firebaseID": driver.user.firebaseID,
                            "acive":driver.user.is_active,
                             "log":driver.user.point_actuelle.log,
                             "alt":driver.user.point_actuelle.alt,
                            
    }
def clientTodict(client):
    return {                "id":         client.id , 
                            "username":   client.user.username,
                            "first_name": client.user.first_name,
                            "last_name":  client.user.last_name,
                            #"email": client.user.email,
                            "typeCompte": client.user.typeCompte,
                            "firebaseID": client.user.firebaseID,
                            "typeclient": client.typeclient,
                            #"log":client.user.point_actuelle.log,
                            #"alt":client.user.point_actuelle.alt,
            }


def coursaCreationTodict(coursa,finished=False):
    coursaSeriliezd ={                "id":coursa.id , 
                            "date_dapart": coursa.date_dapart,
                            "depart": (coursa.depart.alt,coursa.depart.log),
                            "arrive": (coursa.arrive.alt,coursa.arrive.log),
                            "cheufeur":coursa.voiture.id_driver.user.first_name+" "+  coursa.voiture.id_driver.user.last_name
                            #"firebaseIDDriver":
                        }
    if finished:
        coursaSeriliezd['date_arrive']=coursa.date_arrive
    return coursaSeriliezd

