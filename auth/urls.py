from django.urls import path
from auth.views import GetTokenView, RefreshTokenView, LogoutView

app_name = "auth"

urlpatterns = [
    path("token/", GetTokenView.as_view(), name="token"),
    path("token/refresh/", RefreshTokenView.as_view(), name="refresh_token"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
