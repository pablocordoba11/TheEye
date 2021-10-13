from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session as SessionDjango
import random
import string

# Create your models here.
#This is an extension of the User model that django provided. We need to add more detail to our user, 
# in this case we are just adding the token prop to persist it
class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150, null=False, blank=False)

class TimeStampBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#The session will have related the userExtension that also have the token
class Session(TimeStampBase):
    user = models.ForeignKey(UserExtension, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
class EventType(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Application(models.Model):
    def default_secret_key():
        return ''.join(random.sample(string.ascii_letters, 30))

    name = models.CharField(max_length=60, null=False, blank=False)
    url = models.CharField(max_length=80, null=False, blank=False)
    description = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=80, null=True, blank=True)
    app_secret = models.CharField(max_length=30, null=False, blank=False, default=default_secret_key())

    def __str__(self):
        return self.name


class Event(TimeStampBase):
    name = models.CharField(max_length=150, null=False, blank=False)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name='type_set')
    session_django = models.ForeignKey(SessionDjango, on_delete=models.SET_NULL, null=True, blank=True, related_name='session_set')
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='application_set')
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField()

    def __str__(self):
        return self.name + self.type.name
