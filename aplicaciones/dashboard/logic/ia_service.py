import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

def call_ai_api(text):
    """
    Llama a la API de Gemini para evaluar el texto del estudiante.
    Devuelve un diccionario con 'nivel' y 'recomendaciones'.
    """
    API_KEY = os.getenv('API_KEY')
    API_PROVIDER = os.getenv('API_PROVIDER', '').lower()

    if API_PROVIDER != 'gemini' or not API_KEY:
        raise ValueError("El proveedor de IA no está configurado como 'gemini' o falta la API_KEY.")

    # URL de la API de Gemini
    URL_BASE_CORRECTA = "https://generativelanguage.googleapis.com/v1beta/models"
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    gemini_url = f"{URL_BASE_CORRECTA}/{model_name}:generateContent"

    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}

    prompt = (
        f"Eres un experto en diagnóstico académico de Cálculo. "
        f"Evalúa la siguiente respuesta del estudiante basada en su profundidad, corrección de conceptos y claridad. "
        f"Clasifica su nivel de comprensión en una de estas categorías: 'Básico', 'Intermedio' o 'Avanzado'. "
        f"Luego, proporciona 3 recomendaciones concretas y concisas basadas en ese nivel. "
        f"Responde **SOLAMENTE** en formato JSON válido, usando las siguientes claves: "
        f"\"nivel\" (string: Básico|Intermedio|Avanzado), y \"recomendaciones\" (string: lista de recomendaciones separadas por | )."
        f"\n\nRespuesta del estudiante:\n\n{text}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    try:
        resp = requests.post(gemini_url, headers=headers, params=params, json=payload, timeout=45)
        resp.raise_for_status()

        data = resp.json()
        json_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        result = json.loads(json_text)

        recomendaciones_str = result.get('recomendaciones', 'No se recibieron recomendaciones.')
        recomendaciones_lista = [rec.strip() for rec in recomendaciones_str.split('|')]

        return {
            "nivel": result.get('nivel', 'Intermedio'),
            "recomendaciones": recomendaciones_lista
        }

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Falló la llamada a la API. {e}")
        raise ConnectionError(f"No se pudo conectar con el servicio de IA. Inténtalo más tarde.")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"ERROR: Falló el procesamiento de la respuesta de la API. {e}")
        raise ValueError("La respuesta del servicio de IA no tuvo el formato esperado.")


def is_allowed_topic(text):
    """Función de validación simple para asegurar que el tema es relevante."""
    if not text:
        return False
    t = text.lower()
    keywords = ['límite', 'derivada', 'integral', 'cálculo', 'función', 'continuidad']
    return any(kw in t for kw in keywords)