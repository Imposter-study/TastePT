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
    path("social/signin/<str:provider>/", views.SocialSigninView.as_view()),
    path("social/callback/<str:provider>", views.SocialCallbackView.as_view()),
    path("verify-email/<uuid:token>/", views.verify_email, name="verify-email"),
    path("<str:nickname>/", views.ProfileAPIView.as_view()),
]
