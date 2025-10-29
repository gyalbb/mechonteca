#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pathlib


def main():
    """Run administrative tasks."""
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # 2. INICIO DEL CAMBIO CRUCIAL:
    # Agrega la carpeta 'aplicaciones' al path de Python.
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR / 'aplicaciones'))
    # 3. FIN DEL CAMBIO CRUCIAL

    # Establece el módulo de configuración del proyecto como 'config.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
