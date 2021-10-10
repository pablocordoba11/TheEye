from django.urls import path

from . import views

urlpatterns = [
    path('track-post/<str:url>/', views.track_post_request),
    path('auth-user-by-app/', views.get_user_token.as_view()),
]