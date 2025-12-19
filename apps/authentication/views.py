# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from apps.home.models import Perfil
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # 👉 TODOS VAN AL MISMO DASHBOARD
                return redirect("dashboard")

            else:
                msg = "Credenciales incorrectas"
        else:
            msg = "Formulario inválido"

    return render(request, "accounts/login.html", {
        "form": form,
        "msg": msg
    })

from django.shortcuts import render, redirect
from .forms import SignUpForm
from apps.home.models import Perfil

def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validaciones
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Crear perfil
        Perfil.objects.create(
            user=user,
            rol="usuario"  # rol por defecto
        )

        messages.success(request, "Cuenta creada correctamente")
        return redirect("login")

    return render(request, "home/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")
