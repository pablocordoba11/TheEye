from django.urls import path

from . import views

urlpatterns = [
    path('track_request/', views.track_request),
    path('create_even_type/', views.create_even_type),
    path('auth-user-by-app/', views.get_user_token.as_view()),
]