from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegisterView.as_class_view(), name="register"),
    path("login/", UserLoginView.as_class_view(), name="login"),
    path("logout/", UserLogoutView.as_class_view(), name="logout"),
]

