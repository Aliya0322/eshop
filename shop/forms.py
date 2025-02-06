from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Fields in the form: {list(self.fields.keys())}")  # Вывод списка полей в консоль
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None


# class UserAuthForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Пароль", strip=False)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print(f"Fields in the form: {list(self.fields.keys())}")  # ✅ Логирование полей
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = None


class UserAuthForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Пароль", strip=False)