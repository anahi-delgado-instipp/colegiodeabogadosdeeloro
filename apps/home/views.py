
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages

from .models import Evento, Noticia


# ======================================================
#                VISTAS PRINCIPALES (PÁGINAS)
# ======================================================

@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "home/dashboard.html", {'segment': 'dashboard'})


@login_required(login_url="/login/")
def usuarios(request):
    return render(request, "home/usuarios.html", {'segment': 'usuarios'})


@login_required(login_url="/login/")
def map(request):
    return render(request, "home/map.html", {'segment': 'map'})


@login_required(login_url="/login/")
def profile(request):
    return render(request, "home/profile.html", {'segment': 'profile'})


@login_required(login_url="/login/")
def tables(request):
    eventos = Evento.objects.all()
    return render(request, "home/tables.html", {
        "eventos": eventos,
        "segment": "tables"
    })


@login_required(login_url="/login/")
def tablanoticias(request):
    noticias = Noticia.objects.all().order_by('-fecha')
    return render(request, "home/tablanoticias.html", {
        'segment': 'tablanoticias',
        'noticias': noticias
    })


@login_required(login_url="/login/")
def index(request):
    return render(request, "home/index.html", {'segment': 'index'})


# ======================================================
#                     CRUD EVENTOS
# ======================================================

def listar_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'home/tables.html', {
        'eventos': eventos,
        'segment': 'tables'
    })


def guardar_evento(request):
    if request.method == 'POST':
        Evento.objects.create(
            nombre=request.POST['nombre'],
            fecha=request.POST['fecha'],
            hora=request.POST['hora'],
            descripcion=request.POST.get('descripcion', '')
        )
    return redirect('listar_eventos')


def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        evento.nombre = request.POST['nombre']
        evento.fecha = request.POST['fecha']
        evento.hora = request.POST['hora']
        evento.descripcion = request.POST.get('descripcion', '')
        evento.save()

    return redirect('listar_eventos')


def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    return redirect('listar_eventos')


# ======================================================
#                  CRUD NOTICIAS
# ======================================================

def lista_noticias(request):
    noticias = Noticia.objects.all().order_by('-fecha')
    return render(request, "home/tablanoticias.html", {
        "noticias": noticias,
        "segment": "tablanoticias"
    })


def guardar_noticia(request):
    if request.method == "POST":
        imagen = request.FILES.get("imagen")

        noticia = Noticia(
            titulo=request.POST.get("titulo"),
            fecha=request.POST.get("fecha"),
            categoria=request.POST.get("categoria"),
            extracto=request.POST.get("extracto"),
            contenido=request.POST.get("contenido"),
            url=request.POST.get("url") or "",
            imagen=imagen
        )
        noticia.save()

        messages.success(request, "Noticia registrada correctamente.")

    return redirect("tablanoticias")


def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)

    if request.method == "POST":
        noticia.titulo = request.POST.get("titulo")
        noticia.fecha = request.POST.get("fecha")
        noticia.autor = request.POST.get("autor")
        noticia.categoria = request.POST.get("categoria")
        noticia.extracto = request.POST.get("extracto")
        noticia.url = request.POST.get("url")
        noticia.contenido = request.POST.get("contenido")

        if request.FILES.get("imagen"):
            noticia.imagen = request.FILES.get("imagen")

        noticia.save()

        messages.success(request, "Noticia actualizada correctamente.")

    return redirect("tablanoticias")


def eliminar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    noticia.delete()

    messages.success(request, "Noticia eliminada correctamente.")
    return redirect("tablanoticias")


def ver_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(request, "noticias/ver_noticia.html", {
        "noticia": noticia,
        "segment": "tablanoticias"
    })


def pagina_informativa(request):
    eventos = Evento.objects.all()
    return render(request, "pagina_informativa.html", {
        "eventos": eventos,
        "segment": "index"
    })


@login_required(login_url="/login/")
def usuarios(request):
    lista_usuarios = User.objects.all().order_by("username")
    return render(request, "home/usuarios.html", {
        "usuarios": lista_usuarios,
        "segment": "usuarios"
    })


def guardar_usuario(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
        )
    return redirect("usuarios")


def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        usuario.username = request.POST['username']
        usuario.email = request.POST['email']
        usuario.first_name = request.POST.get('first_name', '')
        usuario.last_name = request.POST.get('last_name', '')
        usuario.save()

    return redirect("usuarios")


def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    return redirect("usuarios")
