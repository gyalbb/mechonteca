from django.shortcuts import render
from django.http import HttpResponse

# Vista referenciada por la ruta principal del almacén
def lista_archivos_view(request):
    """
    Vista principal para mostrar la lista de archivos colaborativos.
    """
    # Usamos HttpResponse simple por ahora. 
    # Luego la cambiaremos por render(request, 'almacen/lista_archivos.html', ...)
    return HttpResponse("<h1>Almacén USM: Lista de Archivos (TODO)</h1>")

# Vista referenciada por la ruta de subida de archivos
def subir_archivo_view(request):
    """
    Vista para subir nuevos archivos.
    """
    return HttpResponse("<h1>Almacén USM: Formulario de Subida (TODO)</h1>")

# Create your views here.
