from django.shortcuts import render

def home_view(request):
    # Lógica para la página principal
    return render(request, 'pagina/home.html')

def dashboard_view(request):
    # Lógica para la página del dashboard
    return render(request, 'pagina/dashboard.html')
def ajustes_view(request):
    """Renderiza la página de ajustes."""
    return render(request, 'pagina/ajustes.html', {})

