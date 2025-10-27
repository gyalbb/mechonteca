from django.urls import path
from . import views

urlpatterns = [
    # La página principal
    path('', views.vista_inicio, name='inicio'), 
    # La página de Login
    path('login/', views.vista_login, name='login'), 
    # La página de Registro
    path('registro/', views.vista_registro, name='registro'), 
    # Programas (por ahora usa la misma vista de inicio)
    path('programas/', views.vista_inicio, name='programas'), 
    #ejemplo de latex en html
    path('ejemplo/', views.vista_ejemplo, name="ejemplo")
]