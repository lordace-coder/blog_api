from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token as get_token

urlpatterns = [
    path("get_token/",get_token)
]
