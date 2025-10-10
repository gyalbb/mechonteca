from django.shortcuts import render

# Create your vie# NivelacionUSM/core/views.py

from django.shortcuts import render

def vista_inicio(request):
    # Mostrará el Dashboard Principal (index.html)
    return render(request, 'index.html') 

def vista_login(request):
    # Mostrará la página de Login (login.html)
    return render(request, 'login.html') 

def vista_registro(request):
    # Mostrará la página de Registro (registro.html)
    return render(request, 'registro.html')
