# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Usuario",
            "class": "form-control"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "form-control"
        })
    )


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "form-control"
        })
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repite la contraseña",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Nombres",
                "class": "form-control"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Apellidos",
                "class": "form-control"
            }),
            "username": forms.TextInput(attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Correo electrónico",
                "class": "form-control"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Usuario normal por defecto
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True

        if commit:
            user.save()

        return user
