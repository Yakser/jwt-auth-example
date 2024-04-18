from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from auth.views import GetTokenView, RefreshTokenView

app_name = "auth"

urlpatterns = [
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('token/', GetTokenView.as_view(), name="token"),
    path("token/refresh/", RefreshTokenView.as_view(), name="refresh_token"),
]
