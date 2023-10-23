from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token


class GenerateTokenApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,*args, **kwargs):
        try:
            Token.clear_expired_tokens()
            token =Token.objects.create(user = self.request.user)
            token.save()
            print(token.token)
            return Response(status=201)
        except Exception as err:
            return Response({'error':f"{err}"},status=400)
    
    
    def post(self,*args, **kwargs):
        print(self.request.POST)