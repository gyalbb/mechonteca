from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('diagnostico/<slug:asignatura_slug>/', views.diagnostico_view, name='diagnostico_view'),
    path('formulas/', views.formulas_view, name='formulas_view'),
]