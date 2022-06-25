
from .models import *
import requests
from rest_framework.response import Response


from django.http import JsonResponse

from rest_framework.views import APIView
import json

from django.http import HttpResponse
import requests


from django.views.decorators.csrf import csrf_exempt
key1="key=AAAAvaxaZBI:APA91bFIqn723wmyXXBfbRHQ089WfOH1kCtHiwb58XZ0b1maZC42aG61cb8YFv2kPZ_TVQ7VAfqYmhqyZ7kNOLap_jYCHMX5M1mdMosT9-w0zTjQKLd6y8IZ98fMLQmKTCmWcb_fKvlo"
key='key=AAAAlQ1Lrfw:APA91bHvI2-qFZNCf-oFfeZgM0JUDxxbuykH_ffka9hPUE0xBpiza4uHF0LmItT_SfMZ1Zl5amGUfAXigaR_VcMsEArqpOwHNup4oRTQ24htJ_GWYH0OWZzFrH2lRY24mnQ-uiHgLyln'
    
@csrf_exempt
def notification(request):
    print(request.POST)
    recipient =request.POST['firebaseID']#'Testing1'
    title='notification'
    message = 'corp de notification'
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': key1
        }
    data = {
        "notification": {"title": title, "body": message},
        "to": "/topics/" + recipient,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return HttpResponse("True")



