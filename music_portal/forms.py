import re

from django import forms
from django.contrib.auth.models import User

from .models import MusicRequest, UserProfile

PHONE_PATTERN = re.compile(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$')
NAME_PATTERN = re.compile(r'^[А-Яа-яЁё\s-]+$')


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    full_name = forms.CharField(label='ФИО', max_length=255)
    phone = forms.CharField(label='Телефон', max_length=18, help_text='Формат: 8(XXX)XXX-XX-XX')
    email = forms.EmailField(label='E-mail')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже зарегистрирован.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой e-mail уже зарегистрирован.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not PHONE_PATTERN.match(phone):
            raise forms.ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX.')
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Такой номер телефона уже зарегистрирован.')
        return phone

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        if not NAME_PATTERN.match(full_name):
            raise forms.ValidationError('ФИО должно содержать только кириллицу, пробелы или дефис.')
        return full_name


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class MusicRequestForm(forms.ModelForm):
    class Meta:
        model = MusicRequest
        fields = ['title', 'event_date', 'genre', 'participation_format']
        labels = {
            'title': 'Название проекта или мероприятия',
            'event_date': 'Желаемая дата',
            'genre': 'Жанр музыки',
            'participation_format': 'Формат участия',
        }
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = MusicRequest
        fields = ['status']
        labels = {'status': 'Статус'}
