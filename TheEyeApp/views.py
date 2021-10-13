from django.db.models.query import RawQuerySet
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import exceptions
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ObjectDoesNotExist
import json 
from rest_framework.parsers import JSONParser
from .serializers import *
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class get_user_token(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            app_secret = serializer.initial_data['app_secret']
        except: 
            return HttpResponse({
                "app_secret field is a required parameter in the body of the request"
            }, status=400)
        token = Token.objects.get_or_create(user=user)
        try:
            applcation = Application.objects.get(app_secret=app_secret)
        except ObjectDoesNotExist:
            return HttpResponse({
                "Application resource not found with the provided app secret"
            }, status=404)
        
        #Here we are also starting the session using the django built-in
        #Here we are saving some data to then asociated with the event model
        request.session['username'] = user.username
        request.session["key"] = token[0].key
        request.session['application'] = applcation.name
        request.session.set_expiry(200)
        request.session.__setitem__("test", "value")
        print(str(request.session.get_expiry_age()))
        

        return Response({
            'token': token[0].key,
            'user_id': user.pk,
            'email': user.email,
            'application': applcation.name,
        })



@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def track_request(request):
    try:
        is_token_expired(request.auth.user)
    except Exception as ex:
        return HttpResponse({
                ex
            }, status=400)
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        type_name = serializer.initial_data["category"]
        serializer.initial_data["type"] = serializer.cust_validate_type(type_name)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Action tracked! you can check the values in /admin")
        else:
            return HttpResponse("The date posted is not valid, Here the details: " + str(serializer.errors))


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_event_type(request):
    try:
        is_token_expired(request.auth.user)
    except Exception as ex:
        return HttpResponse({
                ex
            }, status=400)

    if request.method == 'POST':
        serializer = EventTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Event Type Added!")
        else:
            return HttpResponse("The date posted is not valid")        


def is_token_expired(user):
    token = Token.objects.get(user=user)
    time_living = timezone.now() - token.created
    if time_living.seconds > settings.TOKEN_EXPIRATION:
        token.delete()
        raise Exception("Your token is expired! please re-generate it and try again!") 
