from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from core.models import PVData
from .serializers import UserTokenSerializer
from user.models import User
import pandas as pd
from django.db.models import Q
import json
from core.utils import PVPlotly


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


class PVView(APIView):
    @transaction.atomic
    def post(self, request):
        df = pd.read_csv(request.data['file'])
        voltage = df['Tension (V)'].tolist()
        current = df['Corriente (A)'].tolist()
        power = df['Potencia (W)'].tolist()
        temperature = df['Temperatura (°C)'][0]
        module_type = df['Tipo modulo'][0]
        reference = df['Referencia'][0]

        pv_data = PVData.objects.create(
            user=request.user,
            voltage_data=voltage,
            current_data=current,
            power_data=power,
            temperature=temperature,
            module_type=module_type,
            reference=reference,
        )
        return Response(
            {
                'pv_data': pv_data.id
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        id = request.query_params.get('id', None)
        min_temperature = request.query_params.get('min_temperature', None)
        max_temperature = request.query_params.get('max_temperature', None)
        min_date = request.query_params.get('min_date', None)
        max_date = request.query_params.get('max_date', None)
        filters = Q(user=request.user)

        if id:
            filters &= Q(id=id)
        if min_temperature:
            filters &= Q(temperature__gte=min_temperature)
        if max_temperature:
            filters &= Q(temperature__lte=max_temperature)
        if min_date:
            filters &= Q(measure_date__gte=min_date)
        if max_date:
            filters &= Q(measure_date__lte=max_date)

        pv_data = PVData.objects.filter(filters)

        return Response(
            pv_data.values(
                'id',
                'measure_date',
                'module_type',
                'reference',
                'temperature'
            ),
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def put(self, request):
        id = request.data['id']
        measure_date = request.data['measure_date']
        module_type = request.data['module_type']
        reference = request.data['reference']
        temperature = request.data['temperature']
        pv_data = PVData.objects.filter(pk=id).update(
            measure_date=measure_date,
            module_type=module_type,
            reference=reference,
            temperature=temperature
        )

        if pv_data:
            return Response(
                {
                    "id": id,
                    "measure_date": measure_date,
                    "module_type": module_type,
                    "reference": reference,
                    "temperature": temperature,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    @transaction.atomic
    def delete(self, request):
        id = request.data['id']

        pv_data = PVData.objects.get(pk=id).delete()

        if pv_data:
            return Response(
                {
                    "id": pv_data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class PVPlotView(APIView):
    def get(self, request):
        arr_ids = json.loads(request.query_params.get('array', None))
        pv_data = PVData.objects.filter(
            pk__in=arr_ids
        )

        pv_canvas = PVPlotly()
        pv_canvas.add_layout(pv_data.values())
        return Response(
            {
                "canvas": pv_canvas.render_layout()
            },
            status=status.HTTP_200_OK
        )
