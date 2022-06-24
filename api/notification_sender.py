
from .models import *
import requests
from rest_framework.response import Response


from django.http import JsonResponse

from rest_framework.views import APIView
import json


serverToken = "AAAAvaxaZBI:APA91bFIqn723wmyXXBfbRHQ089WfOH1kCtHiwb58XZ0b1maZC42aG61cb8YFv2kPZ_TVQ7VAfqYmhqyZ7kNOLap_jYCHMX5M1mdMosT9-w0zTjQKLd6y8IZ98fMLQmKTCmWcb_fKvlo"

class notifyDriver(APIView):
    def post(self, request):
        #data = json.loads(json.dumps(request.data))
        data={}
        data['client'] = Client.objects.get(id=request.data['client'])
        data['driver'] = Driver.objects.get(id=request.data['driver'])#firebase ID
        data['coursa'] = Coursa.objects.get(id=request.data['coursa'])
        #message=coursa
        response = {}

        if SendToDriver.send_message_to_driver(data['client'].id,
        			        data['driver'].user.firebaseID,
                            str(data['coursa'])
                      		):
            response['success'] = True
        else:
            response['success'] = False

        return JsonResponse(response)


# /message/
class SendToDriver(APIView):
    @staticmethod
    def send_message_to_driver(from_client, to_driver, message):
        finalmsg = {
            'to':  to_driver,
            'data': {
                'message': message,
                'from_user': from_client,
            }
        }

        headers = {
            'Authorization': 'key=' + serverToken,
            'Content-Type': "application/json",
        }

        fcm_response = requests.post('https://fcm.googleapis.com/fcm/send', json.dumps(finalmsg), headers=headers)
        print(fcm_response) 
        print("**************")
        fcm_json_response = json.loads(fcm_response.content)

        if fcm_json_response.has_key('error'):
            return False
        else:
            return True

 