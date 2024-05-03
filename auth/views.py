from django.conf import settings
from django.contrib.auth import authenticate
from drf_yasg import openapi
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import logout


from auth import entities
from drf_yasg.utils import swagger_auto_schema

from auth.serializers import GetTokenSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class GetTokenView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = GetTokenSerializer

    @swagger_auto_schema(
        request_body=GetTokenSerializer,
        responses={200: openapi.Response("Successful response")},
        operation_description="Данный метод в заголовке запроса возвращает access_token."
    )
    def post(self, request):
        response = Response()
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                response['Authorization'] = f'Bearer {data["access"]}'
                return response

            return Response({"detail": entities.Errors.USER_DEACTIVATED.value}, status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": entities.Errors.WRONG_CREDENTIALS.value}, status=status.HTTP_403_FORBIDDEN)


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Response("Successful response")},
        operation_description="Для обновления токена доступа, необходимо, чтобы в Cookie был refresh_token. Данный метод в заголовке запроса возвращает новый access_token."
    )
    def get(self, request, format=None):
        response = Response()

        refresh = RefreshToken(request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME']))

        data = {"access": str(refresh.access_token)}

        # if api_settings.ROTATE_REFRESH_TOKENS:
        #     if api_settings.BLACKLIST_AFTER_ROTATION:
        try:
            # Attempt to blacklist the given refresh token
            refresh.blacklist()
        except AttributeError:
            # If blacklist app not installed, `blacklist` method will
            # not be present
            pass

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        data["refresh"] = str(refresh)
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
            value=data["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response['Authorization'] = f'Bearer {data["access"]}'

        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response("Successful response")},
        operation_description="Завершение сеанса пользователя."
    )
    def post(self, request):
        try:
            try:
                refresh = RefreshToken(request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME']))
                refresh.blacklist()
                logout(request)
            except KeyError:
                return Response(
                    {"error": "Provide refresh_token in data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response = Response({'message': 'Logged out and blacklisted token'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')

            return response
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
