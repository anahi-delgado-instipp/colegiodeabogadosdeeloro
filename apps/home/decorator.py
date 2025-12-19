from django.shortcuts import redirect, render

def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        # Asignar rol según el estado de is_staff
        if request.user.is_staff:
            request.user.perfil.rol = 'admin'  # Admin
        else:
            request.user.perfil.rol = 'visitante'  # Usuario normal

        # Verificar permisos
        if not request.user.is_staff:
            return render(request, 'home/no_permisos.html', status=403)

        return view_func(request, *args, **kwargs)
    return wrapper
