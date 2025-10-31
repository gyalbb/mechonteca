from django.db import models

class Ejercicios(models.Model):
    enunciado = models.CharField(max_length=255)
    ejercicio = models.CharField(max_length=255)
    respuesta_correcta = models.CharField(max_length=255)
    alternativa1 = models.CharField(max_length=255)
    alternativa2 = models.CharField(max_length=255)
    alternativa3 = models.CharField(max_length=255)
    topico = models.CharField(max_length=255)

# Create your models here.
