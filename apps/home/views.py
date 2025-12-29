from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Evento, Noticia, Perfil
from .decorator import solo_admin
from .models import Perfil
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
from django.db.models.functions import ExtractYear
from django.core.mail import send_mail
from .models import Baselegal

# ======================================================
#        VISTAS GENERALES (ADMIN + USUARIO)
# ======================================================

@login_required(login_url="/login/")
def index(request):
    return render(request, "home/index.html", {'segment': 'index'})

@login_required(login_url="/login/")
def dashboard(request):

    # =========================
    # TOTALES
    # =========================
    total_eventos = Evento.objects.count()
    total_noticias = Noticia.objects.count()
    total_usuarios = User.objects.count()

    # =========================
    # USUARIOS
    # =========================
    total_usuarios_activos = User.objects.filter(is_active=True).count()
    total_usuarios_inactivos = User.objects.filter(is_active=False).count()

    # =========================
    # EVENTOS (POR ESTADO)
    # =========================
    total_eventos_proximos = Evento.objects.filter(estado="PROXIMO").count()
    total_eventos_activos = Evento.objects.filter(estado="ACTIVO").count()
    total_eventos_finalizados = Evento.objects.filter(estado="FINALIZADO").count()

    # =========================
    # NOTICIAS
    # =========================
    noticias_publicadas = Noticia.objects.exclude(
        fecha_publicacion__isnull=True
    ).count()

    noticias_sin_fecha = Noticia.objects.filter(
        fecha_publicacion__isnull=True
    ).count()

    # =========================
    # DATOS PARA GRÁFICOS
    # =========================
    usuarios_data = json.dumps([
        total_usuarios_activos,
        total_usuarios_inactivos
    ])

    eventos_data = json.dumps([
        total_eventos_proximos,
        total_eventos_finalizados
    ])

    noticias_data = json.dumps([
        noticias_publicadas,
        noticias_sin_fecha
    ])

    # =========================
    # CONTEXTO
    # =========================
    context = {
        "total_eventos": total_eventos,
        "total_noticias": total_noticias,
        "total_usuarios": total_usuarios,

        "total_usuarios_activos": total_usuarios_activos,
        "total_usuarios_inactivos": total_usuarios_inactivos,

        "total_eventos_proximos": total_eventos_proximos,
        "total_eventos_activos": total_eventos_activos,
        "total_eventos_finalizados": total_eventos_finalizados,

        "usuarios_data": usuarios_data,
        "eventos_data": eventos_data,
        "noticias_data": noticias_data,
    }

    return render(request, "home/dashboard.html", context)


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
        estado=request.POST.get("estado")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active = True if request.POST.get("estado") == "ACTIVO" else False
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
        usuario.first_name = request.POST.get("first_name")
        usuario.last_name = request.POST.get("last_name")

        estado = request.POST.get("estado")
        usuario.is_active = True if estado == "ACTIVO" else False

        if request.POST.get("password"):
            usuario.set_password(request.POST.get("password"))

        usuario.save()
        messages.success(request, "Usuario actualizado")
        return redirect("usuarios")

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

    # ✅ SI NO EXISTE PERFIL, SE CREA
    perfil, created = Perfil.objects.get_or_create(user=user)

    if request.method == 'POST':
        # =====================
        # USUARIO
        # =====================
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # =====================
        # PERFIL
        # =====================
        perfil.telefono = request.POST.get('telefono')
        perfil.cedula = request.POST.get('cedula')
        perfil.direccion = request.POST.get('direccion')

        fecha = request.POST.get('fecha_nacimiento')
        perfil.fecha_nacimiento = fecha if fecha else None

        if request.FILES.get('foto'):
            perfil.foto = request.FILES.get('foto')

        if request.FILES.get('portada'):
            perfil.portada = request.FILES.get('portada')

        perfil.save()

        messages.success(request, "Perfil actualizado correctamente")
        return redirect('profile')

    return render(request, 'home/profile.html', {
        'perfil': perfil
    })


# ======================================================
#        RECUPERAR CONTRASEÑA
# ======================================================

def password_reset_request(request):
    """Maneja la solicitud de recuperación de contraseña, buscando el email en la DB."""
    
    context = {}
    
    if request.method == 'POST':
        user_email = request.POST.get('email', '').strip().lower()
        
        if not user_email:
            context['error'] = "Por favor, ingresa un correo electrónico."
            return render(request, 'autenticacion/password_reset_form.html', context)
        
        # 1. BÚSQUEDA EN LA BASE DE DATOS (Interacción con la DB)
        try:
            # Buscamos el usuario por el campo 'email' en el modelo User
            user = User.objects.get(email=user_email) 
            
            # --- Criterio 1: Usuario Encontrado (Éxito) ---
            
            # 2. ENVÍO DE CORREO REAL
            send_mail(
                subject='Recuperación de Contraseña - FETM',
                # NOTA: Este mensaje NO es un enlace real de Django, es un placeholder.
                message=f'Hola {user.first_name}, hemos recibido una solicitud para restablecer tu contraseña. Haz clic en el siguiente enlace simulado para continuar: http://127.0.0.1:8000/autenticacion/password/done/',
                # ✅ Remitente seguro leído desde settings (EMAIL_HOST_USER)
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=[user_email],
                fail_silently=False, 
            )
            
            # Criterio de Aceptación: Mostrar mensaje de éxito en la interfaz
            context['message'] = "Su contraseña generada ha sido enviada al email ingresado."
            
        except User.DoesNotExist:
            # --- Criterio 2: Usuario No Encontrado (Fallo) ---
            
            # Criterio de Aceptación: Mostrar mensaje de error en la interfaz
            context['error'] = "El correo electrónico ingresado no se encuentra registrado."
            
        return render(request, 'autenticacion/password_reset_form.html', context)
    
    return render(request, 'autenticacion/password_reset_form.html', context)


def password_reset_confirm(request):
    """Simula la interfaz a la que llega el usuario para ingresar la clave temporal/nueva."""
    return render(request, 'autenticacion/password_reset_confirm.html', {})

# ======================================================
#        BASE LEGAL (SOLO ADMIN)
# ======================================================

@login_required(login_url="/login/")
def tabladocumentos(request):
    documentos = Baselegal.objects.all().order_by('-fecha')

    return render(request, "home/tabladocumentos.html", {
        "documentos": documentos,
        "segment": "tabladocumentos"
    })

def biblioteca_legal(request):
    documentos = Baselegal.objects.all()
    return render(request, 'informativa/biblioteca_legal.html', {
        'documentos': documentos
    })



@login_required(login_url="/login/")
@solo_admin
def guardar_documento(request):
    if request.method == "POST":
        archivo = request.FILES.get("archivo")

        # Validar que sea PDF
        if archivo and not archivo.name.lower().endswith(".pdf"):
            messages.error(request, "Solo se permiten archivos PDF")
            return redirect("tabladocumentos")


        Baselegal.objects.create(
            tipo=request.POST.get("tipo"),
            tema=request.POST.get("tema"),
            descripcion=request.POST.get("descripcion"),
            archivo=archivo
        )

        messages.success(request, "Documento registrado correctamente")

    return redirect("tabladocumentos")



@login_required(login_url="/login/")
@solo_admin
def editar_documento(request, documento_id):
    documento = get_object_or_404(Baselegal, id=documento_id)

    if request.method == "POST":
        documento.tipo = request.POST.get("tipo")
        documento.tema = request.POST.get("tema")
        documento.descripcion = request.POST.get("descripcion")

        if request.FILES.get("archivo"):
            # eliminar archivo anterior
            documento.archivo.delete(save=False)
            documento.archivo = request.FILES.get("archivo")

        documento.save()
        messages.success(request, "Documento actualizado correctamente")

    return redirect("tabladocumentos")


@login_required(login_url="/login/")
@solo_admin
def eliminar_documento(request, documento_id):
    documento = get_object_or_404(Baselegal, id=documento_id)

    # eliminar archivo físico
    documento.archivo.delete(save=False)
    documento.delete()

    messages.success(request, "Documento eliminado correctamente")
    return redirect("tabladocumentos")


