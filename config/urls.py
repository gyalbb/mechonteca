"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Logout accesible vía GET y redirige a la raíz — útil para enlaces globales
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # Ruta principal (la raíz '/') es gestionada por la aplicación 'pagina'
    path('', include('aplicaciones.pagina.urls')), 
    
    # La ruta '/almacen/' es gestionada por la app almacen
    path('almacen/', include('aplicaciones.almacen.urls')),
    path('api/', include('aplicaciones.api.urls')),
    # Rutas de autenticación (login, logout, password reset, ...)
    path('accounts/', include('django.contrib.auth.urls')),
]
