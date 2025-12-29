from django.urls import path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.authentication.forms import CustomSetPasswordForm, CustomPasswordResetForm


urlpatterns = [

    # Generales
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map, name='map'),
    path('profile/', views.profile, name='profile'),
    path('tables/', views.tables, name='tables'),
    path('tablanoticias/', views.tablanoticias, name='tablanoticias'),
    path('biblioteca-legal/', views.biblioteca_legal, name='biblioteca_legal'),

    # Recuperar Contraseña
     # 2.1 Pide el correo electrónico (Usaremos tu plantilla 'password_reset_form.html')
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html', # La plantilla que pide el email
            email_template_name='accounts/password_reset_email.html', # El contenido del correo
            subject_template_name='accounts/password_reset_subject.txt', # El asunto
            success_url='done/', # Redirecciona a la ruta 'password_reset_done' definida abajo,
            form_class=CustomPasswordResetForm # <-- Aquí asignamos tu formulario
        ), 
        name='password_reset'
    ),
    
    # 2.2 Mensaje de éxito tras enviar el correo
    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html' # Plantilla que informa que se envió el correo
        ), 
        name='password_reset_done'
    ),
    
    # 2.3 Formulario para ingresar la nueva contraseña (Contiene el token y uidb64)
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             form_class=CustomSetPasswordForm # <-- Aquí asignamos tu formulario
         ), 
         name='password_reset_confirm'
    ),
    
    # 2.4 Confirmación final (Contraseña cambiada con éxito)
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html' # Plantilla de éxito final
        ), 
        name='password_reset_complete'
    ),
 
    # Eventos (ADMIN)
    path('guardar-evento/', views.guardar_evento, name='guardar_evento'),
    path('editar-evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar-evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),

    # Noticias (ADMIN)
    path('noticias/guardar/', views.guardar_noticia, name='guardar_noticia'),
    path('noticias/editar/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/eliminar/<int:noticia_id>/', views.eliminar_noticia, name='eliminar_noticia'),

    # Usuarios (ADMIN)
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/guardar/', views.guardar_usuario, name='guardar_usuario'),
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Perfil
    path('profile/', views.profile, name='profile'),

    # Base Legal (ADMIN)
    path('tabladocumentos/', views.tabladocumentos, name='tabladocumentos'),
    path('documentos/guardar/', views.guardar_documento, name='guardar_documento'),
    path('documentos/editar/<int:documento_id>/', views.editar_documento, name='editar_documento'),
    path('documentos/eliminar/<int:documento_id>/', views.eliminar_documento, name='eliminar_documento'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
