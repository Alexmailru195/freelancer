from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ✅ Регистрация прошла — перенаправляем на вход
            return JsonResponse({
                'success': True,
                'redirect_url': '/accounts/login/'  # ← URL входа
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # ✅ Вход успешен — перенаправляем на главную
            return JsonResponse({
                'success': True,
                'redirect_url': '/'  # ← Главная страница
            })
        else:
            return JsonResponse({'success': False, 'error': 'Неверный логин или пароль'}, status=400)
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('dashboard')