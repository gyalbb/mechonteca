from django.urls import path
from . import views

app_name = 'ejercicios'

urlpatterns = [
    # URL para la página principal de ejercicios (donde se crean o buscan pruebas)
    path('', views.ejercicios_index, name='ejercicios_index'),
    # URL para procesar la creación de una nueva prueba
    path('crear-prueba/', views.crear_prueba, name='crear_prueba'),
    # URL para mostrar la lista de pruebas de un usuario
    path('lista-pruebas/', views.lista_pruebas, name='lista_pruebas'),
    # URL para ver una prueba específica
    path('obtener-prueba/', views.obtener_prueba, name='obtener_prueba'),
    # URL para guardar las respuestas de una prueba
    path('guardar-prueba/', views.guardar_prueba, name='guardar_prueba'),
]