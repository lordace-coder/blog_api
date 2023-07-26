from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post
from .serializers import PostDetailSerializer, PostListSerializers


@api_view(['GET'])
def index(request):
    return Response('hello')


class PostsApiView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializers
    queryset = Post.objects.all()


class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def get_object(self):
        session = self.request.session
        obj = super().get_object()
        if 'viewed' in session:
            if not obj.id in session['viewed']:
                session['viewed'].append(obj.id)
                obj.view_post()
                session.modified = True

        else:
            session['viewed'] = list()
            session['viewed'].append(obj.id)
            obj.view_post()
            session.modified = True
        return obj
