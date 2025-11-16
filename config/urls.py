from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Importar vistas de la app 'pagina'
from aplicaciones.pagina import views as pagina_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de la aplicación principal 'pagina'
    path('', pagina_views.index, name='index'),
    path('signup/', pagina_views.signup, name='signup'),
    path('mi-cuenta/', pagina_views.mi_cuenta, name='mi_cuenta'),
    path('ajustes/', pagina_views.ajustes_view, name='ajustes'),


    # Rutas de la aplicación 'recursos' (Biblioteca)
    path('biblioteca/', include('aplicaciones.recursos.urls')), # Aseguramos que la URL base sea 'biblioteca/'

    # Rutas para la nueva aplicación 'dashboard'
    path('dashboard/', include('aplicaciones.dashboard.urls')),

    # Rutas para la nueva aplicación 'ejercicios'
    path('ejercicios/', include('aplicaciones.ejercicios.urls')),

    # Rutas de autenticación de Django
    path('login/', auth_views.LoginView.as_view(
        template_name='aplicaciones/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Servir archivos media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)