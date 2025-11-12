# Plataforma de Estudio/Nivelacion 

Este es un proyecto web desarrollado con Django, diseñado como una plataforma inteligente para ayudar a los estudiantes a prepararse en diferentes asignaturas de primer año(por el momento solo Calculo).

## Características Principales

**Diagnóstico con IA**: Un sistema que utiliza la API de Gemini para analizar la autoevaluación de un estudiante y asignarle un nivel de conocimiento (Básico, Intermedio, Avanzado).
**Dashboard Personal**: Una vez que el usuario inicia sesión, accede a un panel de control personalizado.
**Biblioteca de Recursos**: Una sección donde los usuarios pueden subir y consultar materiales de estudio.
**Sistema de Autenticación Completo**: Registro, inicio y cierre de sesión.
**Página de Ajustes**: Una sección para futuras configuraciones de usuario como tema e idioma.
**Diseño Moderno**: Interfaz construida con **Tailwind CSS** para un diseño limpio y responsivo.

## Instalacion y Ejecucion 

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### Prerrequisitos

- **Python 3.x**
- **pip** (el gestor de paquetes de Python)

### Pasos de Instalación

1.  **Clona el repositorio** en tu computadora.

2.  **Abre una terminal** y navega a la carpeta raíz del proyecto:
    ```bash
    cd ruta/a/pagina_v4
    ```

3.  **Crea y activa un entorno virtual** (muy recomendado):
    ```bash
    python -m venv venv
    ```
    - **En Windows**:
    ```bash
    .\venv\Scripts\activate
    ```
    - **En macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```

4.  **Instala las dependencias** del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configura las variables de entorno** para la IA:
    - Dentro de la carpeta `aplicaciones/dashboard/logic/`, crea un archivo llamado `.env`.
    - Abre el archivo `.env` y añade las siguientes líneas, reemplazando `TU_API_KEY_DE_GEMINI` con tu clave real:
    ```
    API_PROVIDER=gemini
    API_KEY=TU_API_KEY_DE_GEMINI
    ```

6.  **Aplica las migraciones** para crear la base de datos y las tablas:
    ```bash
    python manage.py migrate
    ```

7.  **(Opcional) Crea un superusuario** para acceder al panel de administrador de Django:
    ```bash
    python manage.py createsuperuser
    ```

8.  **Inicia el servidor de desarrollo**:
    ```bash
    python manage.py runserver
    ```

9.  ¡Listo! Abre tu navegador y visita `http://127.0.0.1:8000/` para ver la plataforma en acción.