from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegisterForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "phone", "country", "avatar")



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Автоматическая стилизация полей под Bootstrap
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'



    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Пользователь с таким email уже зарегистрирован."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_1")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("⚠️ Пароли не совпадают!")
        return cleaned_data


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Меняем ярлык поля с Username на Email
        self.fields["username"].label = "Электронная почта"
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "email@example.com"
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Сохраняем стилизацию Bootstrap для полей редактирования профиля
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


