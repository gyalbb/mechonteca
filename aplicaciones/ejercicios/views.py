from django.shortcuts import render
from .models import Alternativas, Ejercicios, Preguntas, Pruebas
import random

def index(request):
    return render(request, 'index.html')

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
    ejercicios_todos = list(Ejercicios.objects.all())
    seleccion_ejercicios = random.sample(ejercicios_todos, 15)
    prueba = Pruebas.objects.create(usuario=usuario)
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
                'formula': opcion
            })
            orden += 1
        
        preguntas_template.append({
            'enunciado': ejercicio.enunciado,
            'ejercicio': ejercicio.ejercicio,
            'num_pregunta': pregunta.num_pregunta,
            'alternativas': alternativas,
            'topico': ejercicio.topico
        })
        num_pregunta += 1

    contexto = {
        'prueba': prueba,
        'preguntas': preguntas_template,
    }
    return render(request, 'crear-prueba.html', contexto)