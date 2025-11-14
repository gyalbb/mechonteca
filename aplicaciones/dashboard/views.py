from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random
from aplicaciones.recursos.models import Asignatura, Nivel
from .logic.ia_service import call_ai_api, is_allowed_topic
from django.shortcuts import redirect

@login_required(login_url='login')
def dashboard_view(request):
    # Saludos aleatorios para el usuario.
    saludos = [
        f"¡Qué bueno verte de nuevo, {request.user.username}!",
        f"¡Hola, {request.user.username}! ¿Listo/a para empezar?",
        f"¡Bienvenido/a de vuelta, {request.user.username}! ¿Qué haremos hoy?",
        f"Un gusto tenerte aquí, {request.user.username}.",
        f"¡Saludos, {request.user.username}! Tu dashboard te esperaba.",
    ]

    saludo_aleatorio = random.choice(saludos)

    asignaturas = Asignatura.objects.all().order_by('nombre')

    contexto = {
        'titulo_pagina': 'Dashboard',
        'saludo': saludo_aleatorio,
        'asignaturas': asignaturas,
    }
    return render(request, 'dashboard/dashboard.html', contexto)

@login_required(login_url='login')
def diagnostico_view(request, asignatura_slug):
    asignatura = get_object_or_404(Asignatura, slug=asignatura_slug)
    contexto = {
        'titulo_pagina': f'Diagnóstico de {asignatura.nombre}',
        'asignatura': asignatura,
        'resultado': None,
        'error_mensaje': None,
    }

    if request.method == 'POST':
        texto_evaluacion = request.POST.get('autoevaluacion', '').strip()

        # Validaciones
        if len(texto_evaluacion) < 50:
            contexto['error_mensaje'] = "Por favor, proporciona una descripción más detallada (mínimo 50 caracteres)."
            return render(request, 'dashboard/diagnostico.html', contexto)
        
        if not is_allowed_topic(texto_evaluacion):
            contexto['error_mensaje'] = "Tu respuesta no parece estar relacionada con Cálculo. Por favor, enfócate en temas como límites, derivadas o integrales."
            return render(request, 'dashboard/diagnostico.html', contexto)

        # Lógica de IA
        try:
            # Llamada a la API
            resultado_ia = call_ai_api(texto_evaluacion)

            # Búsqueda en BD
            nivel_encontrado = get_object_or_404(Nivel, nombre__iexact=resultado_ia['nivel'])
            
            # Preparar resultado
            contexto['resultado'] = {
                'nivel': nivel_encontrado,
                'recomendaciones': resultado_ia['recomendaciones']
            }

        except Exception as e:
            contexto['error_mensaje'] = f"Hubo un error al procesar tu diagnóstico: {e}. Por favor, inténtalo de nuevo más tarde."

    return render(request, 'dashboard/diagnostico.html', contexto)

@login_required(login_url='login')
def formulas_view(request):
    """Muestra la página de Fórmulas."""
    contexto = {
        'titulo_pagina': 'Formulario de Cálculo',
    }
    return render(request, 'dashboard/formulas.html', contexto)


@login_required(login_url='login')
def ejercitar_view(request):
    """Redirige al índice de la app 'ejercicios'.

    Mantener esta vista en `dashboard` para que la URL
    `/dashboard/ejercitar/` abra la app de ejercicios.
    """
    return redirect('ejercicios:index')
