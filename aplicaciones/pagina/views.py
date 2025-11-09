from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def index(request):
    # Aquí puedes editar la información de tu equipo fácilmente.
    # Las imágenes deben estar en la carpeta 'static/aplicaciones/img/'
    equipo = [
        {
            'id': 'integrante-1',
            'nombre': 'Ángela Ibacache',
            'rol': 'Rol',
            'imagen': 'aplicaciones/img/integrante_1.png',
            'descripcion': 'Descripción del primer integrante.'
        },
        {
            'id': 'integrante-2',
            'nombre': 'Nombre Integrante 2',
            'rol': 'Rol',
            'imagen': 'aplicaciones/img/integrante_2.png',
            'descripcion': 'Descripción del segundo integrante.'
        },
        {
            'id': 'integrante-3',
            'nombre': 'Nombre Integrante 3',
            'rol': 'Rol',
            'imagen': 'aplicaciones/img/integrante_3.png',
            'descripcion': 'Texto sobre el tercer integrante. '
        },
        {
            'id': 'integrante-4',
            'nombre': 'Nombre Integrante 4',
            'rol': 'Rol',
            'imagen': 'aplicaciones/img/integrante_4.png',
            'descripcion': 'Descripción del cuarto integrante. '
        },
        {
            'id': 'integrante-5',
            'nombre': 'Nombre Integrante 5',
            'rol': 'Rol',
            'imagen': 'aplicaciones/img/integrante_5.png',
            'descripcion': 'Descripción del quinto integrante.'
        },
    ]
    return render(request, 'aplicaciones/index.html', {'equipo': equipo})

# Vista para el registro de usuarios
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Inicia sesión automáticamente después del registro
            return redirect('dashboard:dashboard_view') # Redirige al dashboard
    else:
        form = UserCreationForm()
    
    # Añade clases de Tailwind a los campos del formulario para que se vean bien
    form.fields['username'].widget.attrs.update({'class': 'w-full px-3 py-2 border rounded-md mb-4'})
    form.fields['password1'].widget.attrs.update({'class': 'w-full px-3 py-2 border rounded-md mb-4'})
    form.fields['password2'].widget.attrs.update({'class': 'w-full px-3 py-2 border rounded-md'})
    return render(request, 'aplicaciones/signup.html', {'form': form})

@login_required
def mi_cuenta(request):
    return render(request, 'aplicaciones/mi_cuenta.html')

@login_required(login_url='login')
def ajustes_view(request):
    return render(request, 'aplicaciones/ajustes.html')