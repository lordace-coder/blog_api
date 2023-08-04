from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token as get_token

from . import views

urlpatterns = [
    path("get_token/",get_token),
    path("create_user",views.CreateUserView.as_view()),
    path("get_userdata",views.user_info)
]
