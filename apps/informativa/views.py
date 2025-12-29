from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from apps.informativa.models import ContactMessage
from apps.home.models import Baselegal, Evento, Noticia

def pagina_informatica(request):

    eventos = Evento.objects.all().order_by('-fecha_inicio')
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    documentos_base = Baselegal.objects.filter(tipo="Base Legal").order_by('-fecha')
    documentos_biblioteca = Baselegal.objects.filter(tipo="Biblioteca Legal").order_by('-fecha')


    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Guardar en BD
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Mensaje de correo
        mensaje_email = f"""
Nuevo mensaje desde la web

Nombre: {name}
Correo: {email}

Mensaje:
{message}
        """

        # Enviar correo
        send_mail(
            subject=f"Contacto Servicios: {subject}",
            message=mensaje_email,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['colegiodeabo@gmail.com'],
            fail_silently=False,
        )

        # Mensaje flash
        messages.success(request, "¡Tu mensaje fue enviado correctamente!")

        return redirect('pagina_informatica')

    return render(request, 'informativa/pagina_informatica.html', {
        "eventos": eventos,
        "noticias": noticias,
        "documentos_base": documentos_base,
        "documentos_biblioteca": documentos_biblioteca,
    })
