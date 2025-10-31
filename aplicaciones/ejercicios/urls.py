from django.urls import path
from . import views

app_name = 'ejercicios'

urlpatterns = [
    path('', views.ejercicios, name='ejercicios'),
]