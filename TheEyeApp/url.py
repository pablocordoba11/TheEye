from django.urls import path

from . import views

urlpatterns = [
    path('track_request/', views.track_request),
    path('create_event_type/', views.create_event_type),
    path('auth-user-by-app/', views.get_user_token.as_view()),
]