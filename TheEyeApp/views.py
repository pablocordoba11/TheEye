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
from .serializers import *
from django.utils import timezone
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


class get_user_token(ObtainAuthToken):

    @method_decorator(ensure_csrf_cookie)
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
        request.session.save()        

        return Response({
            'token': token[0].key,
            'user_id': user.pk,
            'email': user.email,
            'application': applcation.name,
            'session': request.session.session_key
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
        type_dict = serializer.cust_validate_type(type_name)
        serializer.initial_data["type"] = type_dict

        needs_required = type_dict.get("need_required_field")
        required_fields = type_dict.get("required_fields")

        #Here we are doing validation of the payload depending the type
        validate_payload(needs_required, required_fields, serializer.initial_data["data"])
        #Here we are getting data from the session
        serializer.initial_data["session"] = request.session.session_key
        serializer.initial_data["user_pk"] = request.auth.user.pk
        serializer.initial_data["application_name"] = request.session['application']
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Action tracked! you can check the values in /admin")
        else:
            return HttpResponse("The date posted is not valid, Here the details: " + str(serializer.errors))

def validate_payload(needs_required, fields_to_validate, payload):
    if needs_required:
        required = fields_to_validate.split(",")
        for req in required:
            if not req.strip() in payload:
                raise Exception("Your payload have not all the required fields that the Evend type needs. For: " + fields_to_validate) 

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
