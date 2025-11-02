from django.urls import path
from . import views

app_name = 'ejercicios'

urlpatterns = [
    path('', views.index, name='index'),
    path('ejemplo_ejercicios/', views.ejercicios, name='ejercicios'),
    path('crear-prueba/', views.crear_prueba, name="crear-prueba"),
    path('obtener-prueba/', views.obtener_prueba, name='obtener-prueba'),
    path('guardar-prueba/', views.guardar_prueba, name='guardar-prueba'),
    path('ver-resultados/', views.ver_resultados, name='ver-resultados')
]