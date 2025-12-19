from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Evento, Noticia, Perfil
from .decorator import solo_admin
from .models import Perfil
from django.utils.timezone import now


# ======================================================
#        VISTAS GENERALES (ADMIN + USUARIO)
# ======================================================

@login_required(login_url="/login/")
def index(request):
    return render(request, "home/index.html", {'segment': 'index'})


@login_required(login_url="/login/")
def dashboard(request):
    query = request.GET.get('q')

    if query:
        eventos = Evento.objects.filter(nombre__icontains=query)
    else:
        eventos = Evento.objects.all()

    return render(request, 'home/dashboard.html', {
        'eventos': eventos
    })



@login_required(login_url="/login/")
def map(request):
    return render(request, "home/map.html", {'segment': 'map'})

@login_required(login_url="/login/")
def profile(request):
    user = request.user
    perfil = user.perfil

    if request.method == 'POST':
        # =====================
        # DATOS DEL USUARIO
        # =====================
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # =====================
        # DATOS DEL PERFIL
        # =====================
        perfil.telefono = request.POST.get('telefono')
        perfil.cedula = request.POST.get('cedula')
        perfil.direccion = request.POST.get('direccion')

        fecha = request.POST.get('fecha_nacimiento')
        perfil.fecha_nacimiento = fecha if fecha else None

        # FOTO PERFIL
        if request.FILES.get('foto'):
            perfil.foto = request.FILES.get('foto')

        # FOTO PORTADA 🔥
        if request.FILES.get('portada'):
            perfil.portada = request.FILES.get('portada')

        perfil.save()

        messages.success(request, "Perfil actualizado correctamente")
        return redirect('profile')

    return render(request, 'home/profile.html', {
        'perfil': perfil
    })


@login_required(login_url="/login/")
def tables(request):
    eventos = Evento.objects.all().order_by('-fecha_inicio')

    estado = request.GET.get('estado')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if estado:
        eventos = eventos.filter(estado=estado)

    if desde:
        eventos = eventos.filter(fecha_inicio__gte=desde)

    if hasta:
        eventos = eventos.filter(fecha_fin__lte=hasta)

    return render(request, "home/tables.html", {
        "eventos": eventos
    })





@login_required(login_url="/login/")

@login_required(login_url="/login/")
def tablanoticias(request):
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')

    categoria = request.GET.get('categoria')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if categoria:
        noticias = noticias.filter(categoria__icontains=categoria)

    if desde:
        noticias = noticias.filter(fecha_publicacion__gte=desde)

    if hasta:
        noticias = noticias.filter(fecha_publicacion__lte=hasta)

    return render(request, "home/tablanoticias.html", {
        "noticias": noticias,
        "segment": "tablanoticias"
    })




def ver_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(request, "noticias/ver_noticia.html", {
        "noticia": noticia
    })


# ======================================================
#               EVENTOS (SOLO ADMIN)
# ======================================================

@solo_admin
def guardar_evento(request):
    if request.method == "POST":
        Evento.objects.create(
            nombre=request.POST['nombre'],
            fecha_inicio=request.POST['fecha_inicio'],
            fecha_fin=request.POST['fecha_fin'],
            hora=request.POST['hora'],
            imagen=request.FILES.get('imagen'),
            descripcion=request.POST.get('descripcion', ''),
            estado=request.POST.get('estado', 'PROXIMO')
        )
    return redirect("tables")


@login_required(login_url="/login/")
@solo_admin
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == "POST":
        evento.nombre = request.POST.get('nombre')
        evento.fecha_inicio = request.POST.get('fecha_inicio')
        evento.fecha_fin = request.POST.get('fecha_fin')
        evento.hora = request.POST.get('hora')
        evento.estado = request.POST.get('estado')
        evento.descripcion = request.POST.get('descripcion')

        if request.FILES.get('imagen'):
            evento.imagen = request.FILES['imagen']

        evento.save()
        return redirect('tables')



@login_required(login_url="/login/")
@solo_admin
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    return redirect("tables")


# ======================================================
#               NOTICIAS (SOLO ADMIN)
# ======================================================

@login_required(login_url="/login/")
@solo_admin
def guardar_noticia(request):
    if request.method == "POST":
        Noticia.objects.create(
            titulo=request.POST.get("titulo"),
            fecha_publicacion=request.POST.get("fecha_publicacion"),
            categoria=request.POST.get("categoria"),
            extracto=request.POST.get("extracto"),
            contenido=request.POST.get("contenido"),
            url=request.POST.get("url") or "",
            imagen=request.FILES.get("imagen")
        )
        messages.success(request, "Noticia registrada correctamente")
    return redirect("tablanoticias")


@login_required(login_url="/login/")
@solo_admin
def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)

    if request.method == "POST":
        noticia.titulo = request.POST.get("titulo")
        noticia.fecha_publicacion = request.POST.get("fecha_publicacion")
        noticia.categoria = request.POST.get("categoria")
        noticia.extracto = request.POST.get("extracto")
        noticia.contenido = request.POST.get("contenido")
        noticia.url = request.POST.get("url") or ""

        if request.FILES.get("imagen"):
            noticia.imagen = request.FILES.get("imagen")

        noticia.save()

    return redirect("tablanoticias")


@login_required(login_url="/login/")
@solo_admin
def eliminar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    noticia.delete()
    return redirect("tablanoticias")


# ======================================================
#               USUARIOS (SOLO ADMIN)
# ======================================================

@login_required(login_url="/login/")
@solo_admin
def usuarios(request):
    usuarios = User.objects.all().order_by("username")
    return render(request, "home/usuarios.html", {
        "usuarios": usuarios,
        "segment": "usuarios"
    })


@login_required(login_url="/login/")
@solo_admin
def guardar_usuario(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Usuario creado correctamente")

    return redirect("home/usuarios")


@login_required(login_url="/login/")
@solo_admin
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        usuario.username = request.POST.get("username")
        usuario.email = request.POST.get("email")

        if request.POST.get("password"):
            usuario.set_password(request.POST.get("password"))

        usuario.save()
        messages.success(request, "Usuario actualizado")
        return redirect("home/usuarios")

    return render(request, "home/editar_usuario.html", {
        "usuario": usuario,
        "segment": "usuarios"
    })


@login_required(login_url="/login/")
@solo_admin
def eliminar_usuario(request, user_id):
    try:
        usuario = User.objects.get(id=user_id)
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente")
    except User.DoesNotExist:
        messages.error(request, "El usuario que intentas eliminar no existe")
    return redirect('usuarios')

# ======================================================
#               
# ======================================================
@login_required(login_url="/login/")

def profile(request):
    user = request.user
    perfil = user.perfil

    if request.method == 'POST':
        # Usuario
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Perfil
        perfil.telefono = request.POST.get('telefono')
        perfil.cedula = request.POST.get('cedula')
        perfil.direccion = request.POST.get('direccion')
        perfil.fecha_nacimiento = request.POST.get('fecha_nacimiento')

        if request.FILES.get('foto'):
            perfil.foto = request.FILES.get('foto')

        perfil.save()

        return redirect('profile')

    return render(request, 'home/profile.html')
