from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random
from aplicaciones.recursos.models import Asignatura, Nivel
from .logic.ia_service import call_ai_api, is_allowed_topic

@login_required(login_url='login')
def dashboard_view(request):
    # Lista de saludos aleatorios. Usamos f-strings para incluir el nombre de usuario.
    # request.user está disponible gracias al decorador @login_required.
    saludos = [
        f"¡Qué bueno verte de nuevo, {request.user.username}!",
        f"¡Hola, {request.user.username}! ¿Listo/a para empezar?",
        f"¡Bienvenido/a de vuelta, {request.user.username}! ¿Qué haremos hoy?",
        f"Un gusto tenerte aquí, {request.user.username}.",
        f"¡Saludos, {request.user.username}! Tu dashboard te esperaba.",
    ]

    # Elegimos un saludo al azar de la lista
    saludo_aleatorio = random.choice(saludos)

    # Obtenemos todas las asignaturas para mostrarlas en el dashboard
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

        # --- Validaciones ---
        if len(texto_evaluacion) < 50:
            contexto['error_mensaje'] = "Por favor, proporciona una descripción más detallada (mínimo 50 caracteres)."
            return render(request, 'dashboard/diagnostico.html', contexto)
        
        if not is_allowed_topic(texto_evaluacion):
            contexto['error_mensaje'] = "Tu respuesta no parece estar relacionada con Cálculo. Por favor, enfócate en temas como límites, derivadas o integrales."
            return render(request, 'dashboard/diagnostico.html', contexto)

        # --- Lógica de IA ---
        try:
            # 1. Llamar a la IA
            resultado_ia = call_ai_api(texto_evaluacion)

            # 2. Buscar el nivel en la base de datos
            nivel_encontrado = get_object_or_404(Nivel, nombre__iexact=resultado_ia['nivel'])
            
            # 3. Preparar el resultado para la plantilla
            contexto['resultado'] = {
                'nivel': nivel_encontrado,
                'recomendaciones': resultado_ia['recomendaciones']
            }

        except Exception as e:
            contexto['error_mensaje'] = f"Hubo un error al procesar tu diagnóstico: {e}. Por favor, inténtalo de nuevo más tarde."

    # Para GET o después de POST, renderiza la misma plantilla
    return render(request, 'dashboard/diagnostico.html', contexto)

@login_required(login_url='login')
def niveles_view(request):
    """Muestra la página con la descripción de todos los niveles."""
    niveles = Nivel.objects.all().order_by('id') # Ordenamos por ID para un orden consistente
    contexto = {
        'titulo_pagina': 'Niveles de Conocimiento',
        'niveles': niveles,
    }
    return render(request, 'dashboard/niveles.html', contexto)

@login_required(login_url='login')
def practica_nivel_view(request, nombre_nivel):
    """Muestra la página de práctica para un nivel específico."""
    # Buscamos el nivel en la BD para asegurarnos de que existe
    nivel = get_object_or_404(Nivel, nombre__iexact=nombre_nivel)
    
    # Construimos la ruta de la plantilla dinámicamente
    # Normalizamos el nombre para evitar problemas con caracteres especiales (ej: Básico -> basico)
    nombre_normalizado = nivel.nombre.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    nombre_plantilla = f"dashboard/niveles/{nombre_normalizado}.html"
    
    contexto = {
        'nivel': nivel,
    }
    return render(request, nombre_plantilla, contexto)