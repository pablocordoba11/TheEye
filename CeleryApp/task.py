from CeleryApp.celery import app
import django
django.setup()
from TheEyeApp.views import *
from TheEyeApp.serializers import *
import json


##app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

@app.task(serializer='json')
def celery_track_request(request):

    req_obj = json.loads(request)
    serializer = EventSerializer(data=req_obj.get("data"))
    type_name = serializer.initial_data["category"]
    type_dict = serializer.cust_validate_type(type_name)
    serializer.initial_data["type"] = type_dict

    needs_required = type_dict.get("need_required_field")
    required_fields = type_dict.get("required_fields")

    #Here we are doing validation of the payload depending the type
    validate_payload(needs_required, required_fields, serializer.initial_data["data"])

    #Here we are getting data from the session
    serializer.initial_data["session"] = req_obj.get("session_key")
    serializer.initial_data["user_pk"] = req_obj.get("user_pk")
    serializer.initial_data["application_name"] = req_obj.get("application")
    
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception("The date posted is not valid, Here the details: " + str(serializer.errors))