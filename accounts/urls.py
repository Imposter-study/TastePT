from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignUpAPIView.as_view(), name="signup"),
    path("signin/", views.SignInAPIView.as_view(), name="signin"),
]
