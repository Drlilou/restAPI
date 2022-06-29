
from .models import *
import requests
from rest_framework.response import Response


from django.http import JsonResponse

from rest_framework.views import APIView
import json

from django.http import HttpResponse
import requests
from rest_framework.decorators import api_view


from django.views.decorators.csrf import csrf_exempt
#key1='key=AAAAvaxaZBI:APA91bFIqn723wmyXXBfbRHQ089WfOH1kCtHiwb58XZ0b1maZC42aG61cb8YFv2kPZ_TVQ7VAfqYmhqyZ7kNOLap_jYCHMX5M1mdMosT9-w0zTjQKLd6y8IZ98fMLQmKTCmWcb_fKvlo'
#key ='key=AAAAlQ1Lrfw:APA91bHvI2-qFZNCf-oFfeZgM0JUDxxbuykH_ffka9hPUE0xBpiza4uHF0LmItT_SfMZ1Zl5amGUfAXigaR_VcMsEArqpOwHNup4oRTQ24htJ_GWYH0OWZzFrH2lRY24mnQ-uiHgLyln'
key ="key=AAAAjllUT98:APA91bFxzSxT05hbe-PUMBuTN7a2FdmUJZIACFzUYRxoyW6Jr-fcx5XpbmDSam8JzXHgtAqj2PFOpSuWeRRnI1mhvSnH4hr_K_L4Y-_O2L7XSGOGow_Y4QKnQzyvFt9EoG091Qr-exP3"    
key ="key=AAAAvaxaZBI:APA91bFIqn723wmyXXBfbRHQ089WfOH1kCtHiwb58XZ0b1maZC42aG61cb8YFv2kPZ_TVQ7VAfqYmhqyZ7kNOLap_jYCHMX5M1mdMosT9-w0zTjQKLd6y8IZ98fMLQmKTCmWcb_fKvlo"
@api_view(["POST"])
def notification(request):
    print(request)
    #return HttpResponse(request.data)
    recipient =request.data['firebaseID']#'Testing1'
    #return Response(recipient)
    title='notification'
    message = 'corp de notification'
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': key
        }
    data =  {        "data": {"title": title, "message": message,"lat":36.216755,"lng":2.747962},
        "to": + recipient,
        #"to":"eSk4WK2bPzI:APA91bE2umq01tmLT_Bt8fEuvtuGN8PqtS1jvvic9-Pq0pHGGfGU_cZI6PL3Fwph6jYK7SZPxbLYk08FPBJbDVrHS4YdTFl_Tf8tnJ-psax8radp6aMZPBo-kqOIzJLy68ll8tcnWEXq",
        #"to": "dBkxmIyzADk:APA91bGUl0aEdv2Jr83UbPQuNLPmbjlOKUcHxorX3_2Y_3sT3fdjnRIObOiuuQ3ZKOEiFrjYu_AI5Cj5wBJSUWc4rBn6U1h0D4ZuqVmcPU1Bgav02h39ii-9Seucl7F30dESiwnsX0M3"
        # "to": "/topics/" + recipient,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return Response({"output":response.text})



