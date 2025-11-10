import datetime
from django.shortcuts import get_object_or_404, render
from .models import Alternativas, Ejercicios, Preguntas, Pruebas
import random

def index(request):
    topicos = Ejercicios.objects.values_list('topico', flat=True).distinct().order_by('topico')

    contexto = {
        'topicos': topicos
    }

    return render(request, 'index.html', contexto)
    

# Create your views here.
def ejercicios(request):
    ejercicios = Ejercicios.objects.all()
    seleccionados = random.sample(list(ejercicios), 15)
    seleccion_final = list()
    for seleccionado in seleccionados:
        ejercicio = {
            'enunciado': seleccionado.enunciado,
            'topico': seleccionado.topico,
            'ejercicio': seleccionado.ejercicio,
            'alternativas': [seleccionado.respuesta_correcta, seleccionado.alternativa1, seleccionado.alternativa2]
        }
        random.shuffle(ejercicio['alternativas'])
        seleccion_final.append(ejercicio)
            
    contexto = {
        'ejercicios': seleccion_final
    }

    return render(request, 'ejercicios.html', contexto)

def crear_prueba(request):
    usuario = request.POST.get('username')
    topicos = request.POST.getlist('topicos')
    if len(topicos) == 0:
        topicos = Ejercicios.objects.values_list('topico', flat=True).distinct().order_by('topico')
    seleccion_ejercicios = list(Ejercicios.objects.filter(topico__in=topicos).order_by('?')[:15])
    seleccion_ejercicios.sort(key=lambda x: x.topico)
    prueba = Pruebas.objects.create(usuario=usuario, cantidad_preguntas=15)
    num_pregunta = 1
    preguntas_template = list()
    for ejercicio in seleccion_ejercicios:
        pregunta = Preguntas.objects.create(prueba=prueba, ejercicio=ejercicio, num_pregunta=num_pregunta)
        opciones = [ejercicio.respuesta_correcta, ejercicio.alternativa1, ejercicio.alternativa2]
        random.shuffle(opciones)
        orden = 1
        alternativas = list()
        for opcion in opciones:
            Alternativas.objects.create(pregunta=pregunta, orden=orden, formula=opcion)
            alternativas.append({
                'orden': orden,
                'formula': opcion,
                'seleccionada': False
            })
            orden += 1
        
        preguntas_template.append({
            'id': pregunta.id,
            'respondida': False,
            'enunciado': ejercicio.enunciado,
            'ejercicio': ejercicio.ejercicio,
            'num_pregunta': pregunta.num_pregunta,
            'alternativas': alternativas,
            'topico': ejercicio.topico,
            'respuesta_correcta': None
        })
        num_pregunta += 1

    contexto = {
        'prueba': prueba,
        'preguntas': preguntas_template,
    }
    return render(request, 'crear-prueba.html', contexto)

def obtener_prueba(request):
    prueba_id = request.GET.get('id')
    prueba = get_object_or_404(Pruebas, id=prueba_id)
    preguntas = Preguntas.objects.filter(prueba=prueba).select_related('ejercicio').order_by('num_pregunta')
    preguntas_template = list()
    for pregunta in preguntas:
        alternativas = Alternativas.objects.filter(pregunta=pregunta).order_by('orden').values('formula','orden','seleccionada')
        preguntas_template.append({
            'id': pregunta.id,
            'respondida': pregunta.respuesta != None,
            'enunciado': pregunta.ejercicio.enunciado,
            'ejercicio': pregunta.ejercicio.ejercicio,
            'num_pregunta': pregunta.num_pregunta,
            'alternativas': alternativas,
            'topico': pregunta.ejercicio.topico,
            'respuesta_correcta': pregunta.ejercicio.respuesta_correcta
        })

    contexto = {
        'prueba': prueba,
        'preguntas': preguntas_template,
    }
    return render(request, 'crear-prueba.html', contexto)

def guardar_prueba(request):
    prueba_id = request.POST.get('prueba_id')
    prueba = get_object_or_404(Pruebas, id=prueba_id)

    correctas = 0
    incorrectas = 0

    for item in request.POST.items():
        key, value = item
        if key.startswith('pregunta_'):
            pregunta_id = key.split('_')[1]
            pregunta = get_object_or_404(Preguntas, id=pregunta_id)
            pregunta.respuesta = value
            pregunta.es_correcta = (value == pregunta.ejercicio.respuesta_correcta)
            pregunta.fecha_respuesta = datetime.datetime.now()
            pregunta.save()
            if pregunta.es_correcta:
                correctas += 1
            else:
                incorrectas += 1
            alternativa = get_object_or_404(Alternativas, pregunta=pregunta, formula=value)
            alternativa.seleccionada = True
            alternativa.save()

    prueba.correctas = correctas
    prueba.incorrectas = incorrectas
    prueba.completada = (prueba.cantidad_preguntas == (correctas + incorrectas))
    if prueba.completada:
        prueba.fecha_completada = datetime.datetime.now()
        
    prueba.save()

    contexto = {
        'prueba': prueba,
    }

    return render(request, 'resultados.html', contexto)

def ver_resultados(request):
    prueba_id = request.GET.get('prueba_id')
    prueba = get_object_or_404(Pruebas, id=prueba_id)

    return render(request, 'resultados.html', {'prueba': prueba})

def obtener_pruebas_usuario(request):
    usuario = request.GET.get('username')
    pruebas = Pruebas.objects.filter(usuario=usuario).order_by('id')
    return render(request, 'lista-pruebas.html', {'pruebas': pruebas})
    