from django.urls import path
from . import views

# Es una buena práctica definir el nombre de la app (opcional, pero ayuda)
app_name = 'almacen'

# ESTA LISTA ES EL CONJUNTO DE PATRONES DE URL
urlpatterns = [
    path('', views.lista_archivos_view, name='lista_archivos'),
    path('subir/', views.subir_archivo_view, name='subir_archivo'),
    
    # Por ahora, para simplificar y confirmar la solución, déjala vacía así:
    
] # <--- ¡Debe ser una lista (corchetes)!