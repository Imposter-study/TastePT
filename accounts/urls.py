from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view()),
    path("signin/", views.SignInAPIView.as_view()),
    path("signout/", views.SignOutAPIView.as_view()),
    path("password/", views.PasswordUpdateAPIView.as_view()),
    path("allergies_list/", views.AllergiesListAPIView.as_view()),
    path("preferredCuisine_list/", views.PreferredCuisineListAPIView.as_view()),
    path("random_nickname/", views.CreateRandomNicknameAPIView.as_view()),
    path("auth-check/", views.check_signin_view),
    path("<str:nickname>/", views.ProfileAPIView.as_view()),
]
