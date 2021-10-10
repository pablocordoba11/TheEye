from django.http import HttpResponse, response
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import exceptions
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ObjectDoesNotExist, BadRequest


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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def track_post_request(request):
    print("request")
    req = "all"
    return HttpResponse("TrackingURL!")
