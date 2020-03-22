from rest_framework import serializers
from .models import User, Token


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserAuthBodySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('email', 'password')


class TokenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Token
        fields = 'token',
        extra_kwargs = {'token': {'write_only': True}}


