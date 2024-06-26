from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import api_endpoints

app_name = "users"

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("users/", api_endpoints.UserListAPIView.as_view(), name="user_list"),
]
