# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    descripcion = models.TextField()
    estado = models.CharField(max_length=120, default='PROXIMO')  # PROXIMO, EN_CURSO, FINALIZADO

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    fecha_publicacion = models.DateField(null=True, blank=True)
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
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    cedula = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Baselegal(models.Model):

    TIPO_CHOICES = [
        ('base legal', 'Base Legal'),
        ('biblioteca legal', 'Biblioteca Legal'),
    ]
  
    tema = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='documentos/')
    fecha = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)

    def __str__(self):
        return self.tema
