from django.shortcuts import render, redirect, get_object_or_404 
from django.db.models import Q 
from .models import Material, Asignatura, TipoMaterial 
from .forms import MaterialForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required 


# ---------------- 1. LECTURA (LISTA Y FILTROS) ----------------
def lista_recursos(request):
    
    materiales = Material.objects.all()
    # QuerySets para poblar los filtros en la plantilla
    asignaturas = Asignatura.objects.all().order_by('nombre')
    tipos_material = TipoMaterial.objects.all().order_by('nombre')
    
    query = request.GET.get('q')
    filtro_asignatura = request.GET.get('asignatura') 
    filtro_tipo = request.GET.get('tipo')
    
    # Aplicar filtros
    if query:
        materiales = materiales.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        ).distinct()
    
    if filtro_asignatura:
        materiales = materiales.filter(asignatura__pk=filtro_asignatura)
    
    if filtro_tipo:
        materiales = materiales.filter(tipo_material__pk=filtro_tipo)
    
    contexto = {
        'materiales': materiales,
        'titulo_pagina': 'Biblioteca de Recursos',
        'query': query,
        'asignaturas': asignaturas, 
        'tipos_material': tipos_material, 
        'filtro_asignatura_actual': filtro_asignatura, 
        'filtro_tipo_actual': filtro_tipo 
    }
    
    return render(request, 'recursos/lista_recursos.html', contexto)

# ---------------- 2. CREACIÓN (SUBIR) ----------------
@login_required(login_url='login') 
def crear_recurso(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES) 
        if form.is_valid():
            material = form.save(commit=False) 
            material.subido_por = request.user 
            material.save()
            messages.success(request, '¡Material educativo subido con éxito!')
            return redirect('recursos:lista_recursos')
    else:
        form = MaterialForm()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Subir Nuevo Material',
    }
    
    return render(request, 'recursos/crear_recurso.html', contexto)

# ---------------- 3. EDICIÓN (ACTUALIZAR) ----------------
@login_required(login_url='login')
def editar_recurso(request, pk):
    material = get_object_or_404(Material, pk=pk)
    
    # Seguridad: Solo el usuario que lo subió puede editarlo
    if material.subido_por != request.user:
        messages.error(request, 'No tienes permiso para editar este material.')
        return redirect('recursos:lista_recursos')
        
    if request.method == 'POST':
        # Instancia y FILES son necesarios para editar y manejar el archivo
        form = MaterialForm(request.POST, request.FILES, instance=material) 
        if form.is_valid():
            form.save()
            messages.success(request, f'El recurso "{material.titulo}" ha sido actualizado.')
            return redirect('recursos:lista_recursos')
    else:
        form = MaterialForm(instance=material)
        
    contexto = {
        'form': form,
        'titulo_pagina': 'Editar Material',
        'material': material
    }
    # Reutilizamos la plantilla de creación
    return render(request, 'recursos/crear_recurso.html', contexto)

# ---------------- 4. ELIMINACIÓN (DELETE) ----------------
@login_required(login_url='login')
def eliminar_recurso(request, pk):
    material = get_object_or_404(Material, pk=pk)
    
    # Seguridad: Solo el usuario que lo subió puede eliminarlo
    if material.subido_por != request.user:
        messages.error(request, 'No tienes permiso para eliminar este material.')
        return redirect('recursos:lista_recursos')
        
    if request.method == 'POST':
        # Elimina el archivo físico del disco antes de eliminar el registro
        material.archivo.delete(save=False) 
        material.delete()
        messages.success(request, f'El recurso "{material.titulo}" ha sido eliminado.')
        return redirect('recursos:lista_recursos')
        
    contexto = {
        'material': material,
        'titulo_pagina': 'Confirmar Eliminación'
    }
    return render(request, 'recursos/eliminar_recurso.html', contexto)