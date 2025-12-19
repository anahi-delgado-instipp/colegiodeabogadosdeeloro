from django.shortcuts import render
from apps.informativa.models import ContactMessage
from apps.home.models import Evento, Noticia

def pagina_informatica(request):

    # Cargar eventos y noticias siempre
    eventos = Evento.objects.all().order_by('-fecha_inicio')
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')

    # Si el usuario envía el formulario
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print("POST recibido:", name, email, subject, message)

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render(request, 'informativa/pagina_informatica.html', {
            "success": True,
            "eventos": eventos,
            "noticias": noticias
        })

    # GET normal
    return render(request, 'informativa/pagina_informatica.html', {
        "eventos": eventos,
        "noticias": noticias
    })
