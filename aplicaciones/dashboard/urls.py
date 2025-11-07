from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('diagnostico/<slug:asignatura_slug>/', views.diagnostico_view, name='diagnostico_view'),
    # Nueva ruta para la página de niveles
    path('niveles/', views.niveles_view, name='niveles_view'),
    # Nueva ruta para la página de práctica de cada nivel
    path('niveles/practicar/<str:nombre_nivel>/', views.practica_nivel_view, name='practica_nivel'),
]