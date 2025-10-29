from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Progress
from django.db.utils import OperationalError

def home_view(request):
    # Lógica para la página principal
    return render(request, 'pagina/home.html')

@login_required
def dashboard_view(request):
    # Obtener progreso por usuario para cursos conocidos
    courses = ["Cálculo I", "Álgebra", "Física"]
    course_data = []
    total = 0
    migration_error = False

    try:
        for course in courses:
            try:
                p = Progress.objects.get(user=request.user, course=course)
                percent = p.percent
                topics = p.topics or {}
            except Progress.DoesNotExist:
                percent = 0
                topics = {}
            total += percent
            course_data.append({
                'name': course,
                'percent': percent,
                'topics': topics,
            })

        overall_percent = int(total / len(courses)) if courses else 0
    except OperationalError:
        # La tabla de progreso no existe (migraciones no aplicadas)
        migration_error = True
        course_data = []
        overall_percent = 0

    return render(request, 'pagina/dashboard.html', {
        'overall_percent': overall_percent,
        'courses': course_data,
        'migration_error': migration_error,
    })
def ajustes_view(request):
    """Renderiza la página de ajustes."""
    return render(request, 'pagina/ajustes.html', {})


def signup_view(request):
    """Vista para registrar nuevos usuarios usando UserCreationForm.

    Al crear el usuario, inicia sesión automáticamente y redirige a la raíz.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión al usuario recién creado
            auth_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

