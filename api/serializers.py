from rest_framework import serializers

from .models import *

class TypeUserSerializer(serializers.ModelSerializer):
     class Meta:
        model=Typeuser
        fields='__all__'
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
        fields = "__all__"
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
    #typeuser_name = serializers.RelatedField(source='typeUser', read_only=True)

    class Meta:
        model=Driver
        fields = "__all__"
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(
            username=user_data['username'],email=user_data['email'], password=user_data['password'])
        user_instance.save()
        
        staff_instance = Client.objects.create(
            **validated_data, user=user_instance)
        staff_instance.save()
        return staff_instance


class ClientSignupSerializer(serializers.ModelSerializer):
    typeuser=serializers.CharField(style={"input_type":"select"}   , write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['tlf','typeuser','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['tlf'],
            email=   self.validated_data['tlf'],
            tlf  = self.validated_data['tlf'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.typeCompte='client'
        user.save()
        Client.objects.create(user=user)
        return user
class DriverSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
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

        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.typeCompte='driver'
        user.save()
        Driver.objects.create(user=user)
        return user
