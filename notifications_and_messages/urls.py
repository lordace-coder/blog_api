from django.urls import path

from . import views

urlpatterns = [
    path('',views.NotificationApiView.as_view()),
]
