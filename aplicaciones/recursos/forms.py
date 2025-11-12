from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        # Solo los campos que el usuario debe seleccionar/llenar
        fields = ['titulo', 'descripcion', 'asignatura', 'tipo_material', 'archivo'] 
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'rows': 3}),
            'asignatura': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'tipo_material': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }