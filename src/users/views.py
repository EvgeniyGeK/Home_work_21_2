from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config import settings
from users.forms import UserLoginForm, UserRegisterForm


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        # Сохраняем пользователя в БД
        user = form.save()

        # Автоматически аутентифицируем пользователя после регистрации (опционально)
        # login(self.request, user)

        # Безопасная отправка приветственного письма
        try:
            send_mail(
                subject="Добро пожаловать в наш Интернет-магазин!",
                message=(
                    f"Здравствуйте, {user.email}!\n"
                    f"Вы успешно зарегистрировались на нашем сайте.\n"
                    f"Благодарим за доверие!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Ошибка отправки почты не должна ломать регистрацию пользователя
            print(f"Ошибка при отправке письма: {e}")

        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    # При успешном входе перенаправляем на главную страницу каталога
    success_url = reverse_lazy("catalog:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:home")

