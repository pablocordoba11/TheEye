from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session as SessionDjango
from .models import *

class EventTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False, allow_blank=True, max_length=80)
    description = serializers.CharField(required=False, allow_blank=True, max_length=100)


    def create(self, validated_data):
        return EventType.objects.create(**validated_data)

    class Meta:
        model= EventType
        fields = ('id', 'name', 'description')

class UserSerializer(serializers.Serializer):
    username =  serializers.CharField(required=False, allow_blank=True, max_length=80)

    class Meta:
        model= UserExtension
        fields = ('id', 'name', 'description')

class EventSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    type = EventTypeSerializer(many=False)
    data = serializers.JSONField()
    session = serializers.CharField(required=False, allow_blank=True, max_length=150)
    application_name = serializers.CharField(required=False, allow_blank=True, max_length=60)
    user_pk = serializers.CharField(required=False, allow_blank=True, max_length=60)

    def cust_validate_type(self, value):
        #Here we'll receive the type as a simple string and we need to look for that EventType name
        if type(value) == str:
            try:
                event_type = EventType.objects.get(name=value)
                return event_type.__dict__
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Category name sent is not in the Application")
        else:
            raise serializers.ValidationError("API was expecting a valid Category name")

    def create(self, validated_data):
        event_type = EventType(**validated_data.get("type"))
        session = SessionDjango.objects.get(session_key=validated_data.get("session"))
        user =  User.objects.get(pk=validated_data.get("user_pk"))
        app =  Application.objects.get(name=validated_data.get("application_name"))
        validated_data.pop('type')
        validated_data.pop('application_name')
        validated_data.pop('user_pk')
        validated_data.pop('session')
        return Event.objects.create(type=event_type,session_django=session,user=user,application=app, **validated_data)

    class Meta:
        model= Event
        fields = "__all__"