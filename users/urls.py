from django.urls import path

from users.views import UserDetail, UserList, CurrentUser

app_name = "users"

urlpatterns = [
    path("", UserList.as_view()),
    path("current/", CurrentUser.as_view()),
    path("<int:pk>/", UserDetail.as_view()),
]
