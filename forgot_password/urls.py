from django.urls import path

from .views import GenerateTokenApiView

urlpatterns = [
    path('generate-token',GenerateTokenApiView.as_view(),name='generate-recovery-token'),
]
