from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, MusicRequestForm, RegisterForm, StatusUpdateForm
from .models import MusicRequest, UserProfile

ADMIN_LOGIN = 'BraveGuap'
ADMIN_PASSWORD = 'gosdum'


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
        )
        UserProfile.objects.create(
            user=user,
            full_name=form.cleaned_data['full_name'],
            phone=form.cleaned_data['phone'],
        )
        messages.success(request, 'Регистрация успешна. Теперь войдите в систему.')
        return redirect('login')

    return render(request, 'music_portal/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'music_portal/login.html', {'form': form})


@login_required
def dashboard_view(request):
    requests_qs = request.user.music_requests.all()
    return render(request, 'music_portal/dashboard.html', {'requests': requests_qs})


@login_required
@require_http_methods(['GET', 'POST'])
def create_request_view(request):
    form = MusicRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        music_request = form.save(commit=False)
        music_request.user = request.user
        music_request.status = MusicRequest.STATUS_NEW
        music_request.save()
        messages.success(request, 'Заявка отправлена и получила статус «Новая».')
        return redirect('dashboard')
    return render(request, 'music_portal/create_request.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@require_http_methods(['GET', 'POST'])
def admin_login_view(request):
    if request.session.get('is_admin'):
        return redirect('admin_panel')

    error = None
    if request.method == 'POST':
        login_value = request.POST.get('login', '')
        password_value = request.POST.get('password', '')
        if login_value == ADMIN_LOGIN and password_value == ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('admin_panel')
        error = 'Неверные данные администратора.'

    return render(request, 'music_portal/admin_login.html', {'error': error})


def admin_logout_view(request):
    request.session.pop('is_admin', None)
    return redirect('admin_login')


@require_http_methods(['GET', 'POST'])
def admin_panel_view(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    if request.method == 'POST':
        item = get_object_or_404(MusicRequest, id=request.POST.get('request_id'))
        form = StatusUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус заявки обновлён.')
            return redirect('admin_panel')

    all_requests = MusicRequest.objects.select_related('user', 'user__profile')
    return render(request, 'music_portal/admin_panel.html', {'requests': all_requests})
