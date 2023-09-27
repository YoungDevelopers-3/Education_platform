from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import SignUpSerializer


class SignUpApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        refresh_token = RefreshToken.for_user(request.user)
        tokens = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }
        serializer.data['tokens'] = tokens
        return Response({
            'data': serializer.data,
            'description': "Emailingizga tasdiqlash kodi yuborildi",
            'status': status.HTTP_201_CREATED
        })
