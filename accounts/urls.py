from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view()),
    path("signin/", views.SignInAPIView.as_view()),
    path("signout/", views.SignOutAPIView.as_view()),
    path("password/", views.PasswordUpdateAPIView.as_view()),
    path("<str:nickname>/", views.ProfileAPIView.as_view()),
]
