from django.db import models

class Ejercicios(models.Model):
    enunciado = models.CharField(max_length=255)
    ejercicio = models.CharField(max_length=255)
    respuesta_correcta = models.CharField(max_length=255)
    alternativa1 = models.CharField(max_length=255)
    alternativa2 = models.CharField(max_length=255)
    alternativa3 = models.CharField(max_length=255)
    topico = models.CharField(max_length=255)
    
class Pruebas(models.Model):
    usuario = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_completada = models.DateTimeField(null=True)
    completada = models.BooleanField(default=False)
    correctas = models.IntegerField(default=0)
    incorrectas = models.IntegerField(default=0)
    cantidad_preguntas = models.IntegerField()

class Preguntas(models.Model):
    prueba = models.ForeignKey(Pruebas, on_delete=models.PROTECT)
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.PROTECT)
    num_pregunta = models.IntegerField()
    respuesta = models.CharField(max_length=255, null=True)
    fecha_respuesta = models.DateTimeField(null=True)
    es_correcta = models.BooleanField(null=True)

class Alternativas(models.Model):
    pregunta = models.ForeignKey(Preguntas, on_delete=models.PROTECT)
    orden = models.IntegerField()
    formula = models.CharField(max_length=255)
    seleccionada = models.BooleanField(default=False)
     
# Create your models here.
