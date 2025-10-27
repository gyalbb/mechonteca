# Diagnóstico — Evaluación de estudiantes

Aplicación web simple (Flask) para enviar texto/respuestas de estudiantes y obtener una evaluación de nivel.

## Requisitos
- Python 3.8+
- Un entorno virtual (recomendado)

## Preparar el entorno
1. Crear y activar el entorno virtual (ejemplo en PowerShell):

```powershell
cd "C:\Users\PC\OneDrive\Desktop\Diagnostico"
python -m venv .venv
# Activar
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias (si no están instaladas):

```powershell
pip install -r requirements.txt
```

3. Variables de entorno: copia `.env` y añade tu API key si vas a usar una API externa.

- Para integración con Hugging Face Inference API, añade en `.env`:

```
API_PROVIDER=huggingface
API_KEY=tu_api_key_de_huggingface
HF_MODEL=nombre/del-modelo
```

- Si prefieres usar otra API, ajusta `API_PROVIDER` y `API_URL` según la documentación.

Si no configuras ninguna API, la aplicación usará un evaluador heurístico local sencillo.

## Ámbito y temas aceptados

Esta herramienta está enfocada a evaluaciones de Cálculo I (nivel universitario). De momento solo se aceptan respuestas relacionadas con estos temas, por ejemplo:

- Proposiciones y lógica básica
- Inecuaciones
- Límites
- Derivadas
- Integrales básicas
- Funciones y análisis de continuidad

Por favor, al rellenar el formulario describe tu comprensión, cómo resuelves problemas y si puedes explicar los pasos.

## Ejecutar la aplicación

```powershell
python app.py
```

Abrir en el navegador: http://localhost:5000

## Estructura
- `app.py` — aplicación Flask y lógica principal
- `templates/index.html` — formulario web
- `static/style.css` — estilos
- `.env` — configuración de claves (NO subir a git)

## Mejoras posibles
- Añadir autenticación y una base de datos para guardar resultados
- Usar un modelo de clasificación afinado para evaluación (Hugging Face / API externa)
- Añadir tests automáticos

Si quieres, puedo:
- Integrar con una API específica (por ejemplo, Hugging Face) usando un modelo de clasificación y mostrar cómo interpretar la respuesta
- Añadir validaciones al formulario, más campos, y una vista de historial
