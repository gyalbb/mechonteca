from django.shortcuts import render
from .models import Ejercicios
import random

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