from django.urls import path
from . import views

app_name = 'recursos'

urlpatterns = [
    # CRUD: Leer (Lista)
    path('', views.lista_recursos, name='lista_recursos'),
    # CRUD: Crear (Subir)
    path('subir/', views.crear_recurso, name='crear_recurso'),
    # CRUD: Actualizar (Editar)
    path('editar/<int:pk>/', views.editar_recurso, name='editar_recurso'),
    # CRUD: Eliminar
    path('eliminar/<int:pk>/', views.eliminar_recurso, name='eliminar_recurso'),
]