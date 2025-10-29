from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model
from aplicaciones.pagina.models import Progress
import json

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() 
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                'user': serializer.data,
                'token': token.key
            },
            status=status.HTTP_201_CREATED,  # fixed
            headers=headers
        )



