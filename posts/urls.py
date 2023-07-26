from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('posts', views.PostsApiView.as_view()),
    path('post/<int:pk>', views.PostDetailApiView.as_view())
]


urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
