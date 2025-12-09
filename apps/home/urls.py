# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard

urlpatterns = [

    # Dashboard y páginas base
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('map/', views.map, name='map'),
    path('profile/', views.profile, name='profile'),
    path('tables/', views.tables, name='tables'),
    path('tablanoticias/', views.tablanoticias, name='tablanoticias'),

    # Eventos
    path('eventos/', views.listar_eventos, name='listar_eventos'),
    path('guardar-evento/', views.guardar_evento, name='guardar_evento'),
    path('editar-evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar-evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),

    # Noticias
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('noticias/guardar/', views.guardar_noticia, name='guardar_noticia'),
    path('noticias/editar/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/eliminar/<int:noticia_id>/', views.eliminar_noticia, name='eliminar_noticia'),
    path('noticias/ver/<int:noticia_id>/', views.ver_noticia, name='ver_noticia'),

    # Usuarios
    path("usuarios/", views.usuarios, name="usuarios"),
path("usuarios/guardar/", views.guardar_usuario, name="guardar_usuario"),
path("usuarios/editar/<int:user_id>/", views.editar_usuario, name="editar_usuario"),
path("usuarios/eliminar/<int:user_id>/", views.eliminar_usuario, name="eliminar_usuario"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
