import os
import django
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
django.setup()
from aplicaciones.ejercicios.models import Ejercicios
qs = Ejercicios.objects.all()[:20]
for i,e in enumerate(qs,1):
    print('---',i,'id=',e.id,'topico=',repr(e.topico))
    print('enunciado raw repr:',repr(e.enunciado)[:1000])
    print('ejercicio repr:',repr(e.ejercicio)[:1000])
    print()