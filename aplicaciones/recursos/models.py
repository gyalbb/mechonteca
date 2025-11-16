from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Asignatura(models.Model):
    """Representa las asignaturas (ej. 'Cálculo I')."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Asignatura")
    slug = models.SlugField(unique=True, blank=True, max_length=100) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"


class TipoMaterial(models.Model):
    """Representa las subcarpetas (ej. 'Talleres', 'Certámenes')."""
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Material (Subcarpeta)")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Material"
        verbose_name_plural = "Tipos de Material"
        

class Material(models.Model):
    """El recurso o archivo digital en sí."""
    
    # Claves Foráneas para la estructura (Asignatura y Subcarpeta)
    asignatura = models.ForeignKey(
        Asignatura, 
        on_delete=models.CASCADE, 
        verbose_name="Asignatura"
    )
    tipo_material = models.ForeignKey(
        TipoMaterial, 
        on_delete=models.CASCADE, 
        verbose_name="Categoría (Subcarpeta)"
    )
    
    titulo = models.CharField(max_length=150, verbose_name="Título del Recurso")
    descripcion = models.TextField(blank=True, verbose_name="Descripción o Resumen")
    
    # Campo para subir el archivo (PDF, Imagen, etc.)
    archivo = models.FileField(
        upload_to='materiales/',
        verbose_name="Archivo Digital"
    )
    
    # Para la funcionalidad de edición/eliminación (CRUD)
    subido_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Subido por"
    )
    
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.asignatura}] {self.titulo}"
    
    class Meta:
        verbose_name = "Material Educativo"
        verbose_name_plural = "Materiales Educativos"
        ordering = ['asignatura__nombre', 'titulo']

class Nivel(models.Model):
    """Representa los niveles de conocimiento (Básico, Intermedio, Avanzado)."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre