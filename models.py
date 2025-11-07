from django.db import models

class Contenido(models.Model):
    """
    Representa un tema o unidad de la sección de nivelación.
    """
    titulo = models.CharField(max_length=200, verbose_name="Título del Contenido")
    resumen = models.TextField(blank=True, verbose_name="Resumen")

    def __str__(self):
        return self.titulo