from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from core.permissions import IsOwnerOrReadOnly
from users.serializers import UserDetailSerializer, UserListSerializer

User = get_user_model()


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserListSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    serializer_class = UserDetailSerializer


class CurrentUser(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # get refresh token from request body
            try:
                refresh_token = request.data["refresh_token"]
            except KeyError:
                return Response(
                    {"error": "Provide refresh_token in data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # blacklist the refresh token
            RefreshToken(refresh_token).blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
