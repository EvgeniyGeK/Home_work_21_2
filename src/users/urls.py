from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
path('profile/', UserProfileView.as_view(), name='profile')
]

