# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    fecha = models.DateField()
    categoria = models.CharField(max_length=50, blank=True, null=True)
    extracto = models.CharField(max_length=200, blank=True, null=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias/', null=True, blank=True)
    url = models.URLField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

