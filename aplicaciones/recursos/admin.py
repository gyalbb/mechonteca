from django.contrib import admin

# Register your models here.
from .models import Material, Asignatura, TipoMaterial, Nivel

# ---------------- Administración de Jerarquía ----------------
admin.site.register(Asignatura)
admin.site.register(TipoMaterial)
admin.site.register(Nivel)


# ---------------- Administración de Material ----------------
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'asignatura', 'tipo_material', 'subido_por', 'fecha_subida', 'archivo')
    list_filter = ('asignatura', 'tipo_material', 'fecha_subida')
    search_fields = ('titulo', 'descripcion', 'asignatura__nombre')

admin.site.register(Material, MaterialAdmin)