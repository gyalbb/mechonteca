from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('ajustes/', views.ajustes_view, name='ajustes'),
]