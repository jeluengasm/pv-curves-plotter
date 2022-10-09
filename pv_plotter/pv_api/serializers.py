from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import PVData


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UploadFileSerializer(serializers.Serializer):
    class Meta:
        model = PVData
        fields = '__all__'
