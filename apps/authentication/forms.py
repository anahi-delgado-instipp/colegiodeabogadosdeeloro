# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.core.exceptions import ValidationError


# ======================
# LOGIN
# ======================
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


# ======================
# REGISTRO
# ======================
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
        fields = ("first_name", "last_name", "username", "email")
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
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True

        if commit:
            user.save()
        return user


# ======================
# CAMBIAR CONTRASEÑA (LINK DEL EMAIL)
# ======================
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
        })


# ======================
# RESET POR CORREO
# ======================
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        UserModel = get_user_model()

        if not UserModel.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("El correo electrónico no se encuentra registrado.")

        return email
