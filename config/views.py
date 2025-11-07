from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Asignatura

@login_required
def lista_recursos(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'aplicaciones/recursos/lista_recursos.html', {'asignaturas': asignaturas})