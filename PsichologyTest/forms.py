from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import password_validation
from django import forms
import re


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'second_name', 'middle_name', 'date_of_birth', 'email', 'phone_number',
                  'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        password_validation.validate_password(password2, self.instance)

        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = re.compile(r'^\+?1?\d{9,15}$')

        if not pattern.match(phone_number):
            raise forms.ValidationError('Некорректный формат номера телефона.', code='invalid_phone_number')

        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.second_name = self.cleaned_data['second_name']
        if commit:
            user.save()
        return user

