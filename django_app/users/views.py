import jwt
from django.conf import settings
from django.contrib.auth import user_logged_in
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, UserAuthBodySerializer, TokenSerializer


class CreateUserAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RefreshToken(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserAuthBodySerializer

    @swagger_auto_schema(operation_description="Получение токена авторизации",
                         responses={200: openapi.Response('Токен авторизации', TokenSerializer)})
    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']

            user = User.objects.get(email=email, password=password)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {'token': token}
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllUsersAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = [self.serializer_class(user).data for user in users]

        return Response(serializer, status=status.HTTP_200_OK)
