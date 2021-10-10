from django.db import models
from django.contrib.auth.models import User

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
    user = models.OneToOneField(UserExtension, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
class EventType(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Event(TimeStampBase):
    name = models.CharField(max_length=150, null=False, blank=False)
    type = models.OneToOneField(EventType, on_delete=models.CASCADE)
    session_event = models.OneToOneField(Session, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField()

class Application(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    url = models.CharField(max_length=80, null=False, blank=False)
    description = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=80, null=True, blank=True)