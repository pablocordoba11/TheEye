from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import exceptions
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ObjectDoesNotExist
import json 
from rest_framework.parsers import JSONParser
from .serializers import *


class get_user_token(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        app_secret = serializer.initial_data['app_secret']
        token = Token.objects.get_or_create(user=user)
        try:
            applcation = Application.objects.get(app_secret=app_secret)
        except ObjectDoesNotExist:
            return HttpResponse({
                "Application resource not found with the provided app secret"
            }, status=404)
        
        return Response({
            'token': token[0].key,
            'user_id': user.pk,
            'email': user.email,
            'application': applcation.name
        })



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def track_request(request):
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_even_type(request):
    if request.method == 'POST':
        serializer = EventTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Event Type Added!")
        else:
            return HttpResponse("The date posted is not valid")

    