from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

from auth import entities


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class GetTokenView(APIView):
    permission_classes = [AllowAny]
    # todo: serializer
    def post(self, request, format=None):
        response = Response()
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = data
                return response

            return Response({"detail": entities.Errors.USER_DEACTIVATED.value}, status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": entities.Errors.WRONG_CREDENTIALS.value}, status=status.HTTP_403_FORBIDDEN)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    # todo: serializer
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
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=data["access"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
            value=data["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response.data = data
        return response