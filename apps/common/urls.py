from django.urls import path

from . import api_endpoints

app_name = "common"

urlpatterns = [
    path("media-upload/", api_endpoints.MediaCreateAPIView.as_view(), name="media_upload"),
]
