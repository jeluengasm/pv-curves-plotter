from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserTokenSerializer
from user.models import User


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


class RegisterUserView(APIView):

    @transaction.atomic
    def post(self, request):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        username = request.data['username']
        email = request.data['email']
        phone_number = request.data['phone_number']
        password = request.data['password']
        password2 = request.data['password2']

        if password != password2:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            email=email,
            password=password
        )
        # user = None
        if user is None:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone_number=phone_number
            )
            user_serializer = UserTokenSerializer(user)
            return Response(
                {
                    'user': user_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)