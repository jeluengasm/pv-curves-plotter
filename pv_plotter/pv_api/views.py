from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserTokenSerializer


class LoginUserView(APIView):
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        user = authenticate(
            email=request.data['email'],
            password=request.data['password']
        )
        try:
            Token.objects.get(user=user).delete()
        except Token.DoesNotExist:
            pass
        if user is not None:
            login(request, user)
            token = Token.objects.create(user=user)
            user_serializer = UserTokenSerializer(user)
            return Response(
                {
                    'token': token.key,
                    'user': user_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    @transaction.atomic
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
