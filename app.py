from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import math
import re

app = Flask(__name__)
load_dotenv()  # Cargar variables de entorno desde .env

# Leer configuración desde .env
API_KEY = os.getenv('API_KEY', '')
API_URL = os.getenv('API_URL', '')
API_PROVIDER = os.getenv('API_PROVIDER', '').lower()  # 'huggingface', 'deepseek', etc.
HF_MODEL = os.getenv('HF_MODEL', '')  # ejemplo: 'facebook/bart-large-mnli' o un modelo de clasificación


def heuristic_evaluation(text):
    """Evaluador simple si no hay API configurada.
    Usa heurísticas (longitud, vocabulario) para devolver un nivel aproximado.
    """
    if not text:
        return {"nivel": "No definido", "recomendaciones": "No se recibieron respuestas."}

    words = text.split()
    word_count = len(words)
    unique_words = len(set(words))
    avg_word_len = sum(len(w) for w in words) / word_count if word_count else 0

    score = 0
    # Dar puntos por cantidad y diversidad
    score += min(word_count / 50, 1.5)
    score += min(unique_words / 30, 1.0)
    score += min(avg_word_len / 5, 1.0)

    # Escalar a niveles
    if score < 1.5:
        nivel = "Básico"
        rec = "Reforzar conceptos básicos. Trabajar comprensión de lectura y vocabulario."
    elif score < 2.5:
        nivel = "Intermedio"
        rec = "Buen manejo de conceptos. Recomendar práctica guiada y ejercicios de razonamiento."
    else:
        nivel = "Avanzado"
        rec = "Alto nivel. Proponer tareas de síntesis, análisis y problemas aplicados."

    return {"nivel": nivel, "recomendaciones": rec, "meta": {"word_count": word_count, "unique_words": unique_words, "avg_word_len": avg_word_len}}


def call_ai_api(text):
    """Llama a la API configurada. Si no está configurada, usa el evaluador heurístico.
    Soporta una integración básica con la API de Hugging Face (Inference API) si se indica.
    """
    # Si el texto parece ser una lista numerada/bullets con ítems claros, aplicar regla local más específica
    parsed = parse_numbered_items(text)
    if parsed:
        return evaluate_from_items(parsed)

    if API_PROVIDER == 'huggingface' and API_KEY and HF_MODEL:
        hf_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        try:
            # Usar zero-shot: enviar candidate_labels para obtener probabilidades por etiqueta
            payload = {
                "inputs": text,
                "parameters": {
                    "candidate_labels": ["Básico", "Intermedio", "Avanzado"],
                    "multi_label": False
                }
            }
            resp = requests.post(hf_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # Respuesta típica de zero-shot: { labels: [...], scores: [...] }
            if isinstance(data, dict) and 'labels' in data and 'scores' in data:
                labels = data.get('labels', [])
                scores = data.get('scores', [])
                if labels and scores:
                    # Encontrar el índice del score más alto
                    max_score_index = scores.index(max(scores))
                    top_label = labels[max_score_index]
                    top_score = scores[max_score_index]
                    
                    # Generar recomendaciones basadas en el nivel y la confianza
                    recomendaciones = []
                    if top_label == "Básico":
                        recomendaciones.append("Reforzar conceptos fundamentales")
                        recomendaciones.append("Practicar ejercicios básicos con supervisión")
                    elif top_label == "Intermedio":
                        recomendaciones.append("Incrementar complejidad gradualmente")
                        recomendaciones.append("Fomentar pensamiento independiente")
                    else:  # Avanzado
                        recomendaciones.append("Proponer desafíos adicionales")
                        recomendaciones.append("Fomentar investigación y proyectos")
                    
                    return {
                        "nivel": top_label,
                        "confianza": f"{top_score:.2%}",
                        "recomendaciones": " • ".join(recomendaciones),
                        "detalles": {
                            "todos_niveles": list(zip(labels, [f"{s:.2%}" for s in scores]))
                        }
                    }

            # Algunos modelos devuelven una lista de dicts con 'label'/'score'
            if isinstance(data, list) and data and isinstance(data[0], dict) and 'label' in data[0]:
                top = max(data, key=lambda d: d.get('score', 0))
                return {"nivel": top.get('label'), "recomendaciones": f"Confianza: {top.get('score')}"}

            # Si el modelo genera texto, intentar inferir nivel por palabras clave
            if isinstance(data, dict) and 'generated_text' in data:
                gen = data['generated_text']
                if 'básico' in gen.lower() or 'beginner' in gen.lower():
                    nivel = 'Básico'
                elif 'intermedio' in gen.lower() or 'intermediate' in gen.lower():
                    nivel = 'Intermedio'
                else:
                    nivel = 'Avanzado'
                return {"nivel": nivel, "recomendaciones": gen}

            # Fallback a heurística si no entendemos la respuesta
            return heuristic_evaluation(text)
        except Exception as e:
            # Si falla la llamada externa, usar heurística
            return {"error": f"Error llamando a Hugging Face: {str(e)}", **heuristic_evaluation(text)}

    # Si API_URL y API_KEY están configuradas y no se eligió 'huggingface', intentar llamada genérica
    if API_URL and API_KEY:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        try:
            resp = requests.post(API_URL, headers=headers, json={"text": text}, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": f"Error llamando a la API configurada: {str(e)}", **heuristic_evaluation(text)}

    # Fallback local
    return heuristic_evaluation(text)


def is_allowed_topic(text):
    """Verifica si el texto menciona temas de Cálculo I permitidos.
    Retorna True si detecta al menos una palabra clave relevante.
    """
    if not text:
        return False
    t = text.lower()
    # palabras clave relacionadas con Cálculo I
    keywords = [
        'límite', 'limite', 'derivada', 'derivadas', 'integral', 'integrales',
        'inecuación', 'inecuaciones', 'inecuacion', 'inecuaciones',
        'proposición', 'proposicion', 'proposiciones',
        'función', 'funcion', 'funciones', 'continuidad', 'límite', 'sucesión',
        'cálculo', 'calculo', 'derivación', 'derivacion', 'integración', 'integracion'
    ]
    # Buscar palabras completas usando regex para evitar coincidencias parciales
    for kw in keywords:
        if re.search(r"\b" + re.escape(kw) + r"\b", t):
            return True
    return False


def parse_numbered_items(text):
    """Detecta líneas numeradas (1), 2), 3.) o bullets y devuelve lista de ítems si parece un formato de lista.
    Devuelve None si no se detecta un patrón claro.
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    items = []
    for l in lines:
        # patrones: "1)", "1.", "1 -", "1) texto", "• texto"
        if l[0].isdigit() or l.startswith('-') or l.startswith('•'):
            # quitar prefijo numerico o bullet
            # buscar primer espacio después de un número y paréntesis/./-
            if l[0].isdigit():
                # encontrar primera aparición de ')' or '.' or '-'
                sep_pos = None
                for ch in [')', '.', '-']:
                    if ch in l:
                        sep_pos = l.find(ch)
                        break
                if sep_pos is not None and sep_pos + 1 < len(l):
                    items.append(l[sep_pos+1:].strip())
                else:
                    # si no hay separador, tomar todo menos el número
                    items.append(l[1:].strip())
            else:
                # bullet
                items.append(l.lstrip('-•').strip())
        else:
            # si la línea no tiene número ni bullet, verificar si todo el texto es una única línea con comas que parezca items
            pass

    # Si no encontramos ítems por líneas, intentar separar por números en una sola línea
    if not items:
        # buscar "1)" en el texto
        import re
        parts = re.split(r"\b\d+\)\s*", text)
        if len(parts) > 2:
            # partes[0] es prefijo, ignorar
            items = [p.strip() for p in parts[1:] if p.strip()]

    return items if len(items) >= 2 else None


def score_keyword_presence(text, positive_keywords, negative_keywords=None):
    s = 0.0
    t = text.lower()
    for kw in positive_keywords:
        if kw in t:
            s += 1.0
    if negative_keywords:
        for kw in negative_keywords:
            if kw in t:
                s -= 1.0
    # normalizar a 0..1
    # asumir máximo 3 positivos para escalar
    score = max(0.0, min(1.0, 0.25 * s + 0.25))
    return score


def evaluate_from_items(items):
    """Evaluación basada en los ítems esperados:
    ítem 1: comprensión
    ítem 2: resolución de problemas
    ítem 3: explicación/aplicación
    ítem 4: independencia/creatividad
    """
    # Normalizar lista a 4 items (si más, tomar primeros 4; si menos, completar con '' )
    items = (items + [""]*4)[:4]

    # Definir keywords por ítem
    kw = [
        (['entiendo', 'comprendo', 'entiendo muchos', 'puedo entender'], ['dificultad', 'dificultan', 'no entiendo', 'me cuesta']),
        (['resolver', 'resuelvo', 'puedo resolver', 'resoluciones', 'ejercicios'], ['con ayuda', 'ayuda', 'inteligencia artificial', 'no puedo resolver']),
        (['explicar', 'puedo explicar', 'aplicar', 'aplicarlos', 'aplico'], ['no puedo explicar', 'dificulta aplicarlos', 'me cuesta aplicar']),
        (['puedo estudiar por mi', 'independiente', 'investigo', 'busco recursos', 'autodidacta', 'por mi mismo', 'solo'], ['no soy muy bueno', 'con ayuda', 'necesito ayuda', 'dependo de'])
    ]

    scores = []
    for i, it in enumerate(items):
        pos, neg = kw[i]
        sc = score_keyword_presence(it, pos, neg)
        scores.append(sc)

    # Pesos
    weights = [0.3, 0.25, 0.25, 0.2]
    overall = sum(s * w for s, w in zip(scores, weights))

    if overall < 0.4:
        nivel = 'Básico'
    elif overall < 0.7:
        nivel = 'Intermedio'
    else:
        nivel = 'Avanzado'

    recomendaciones = []
    if nivel == 'Básico':
        recomendaciones.append('Reforzar conceptos básicos paso a paso y solicitar ayuda del docente.')
    elif nivel == 'Intermedio':
        recomendaciones.append('Practicar problemas guiados y aumentar la autonomía progresivamente.')
    else:
        recomendaciones.append('Explorar problemas más complejos y proponer proyectos de aplicación.')

    # Explicar independencia y creatividad con más detalle
    independencia_detail = ''
    ind_score = scores[3]
    if ind_score > 0.6:
        independencia_detail = 'Buena independencia: busca recursos, investiga por su cuenta y planifica el estudio.'
    elif ind_score > 0.3:
        independencia_detail = 'Independencia moderada: estudia por su cuenta algunas veces pero suele necesitar guía.'
    else:
        independencia_detail = 'Baja independencia: depende de ayuda externa y necesita entrenamiento en técnicas de estudio.'

    return {
        'nivel': nivel,
        'confianza': f"{overall:.2%}",
        'recomendaciones': ' '.join(recomendaciones) + ' ' + independencia_detail,
        'detalle_items': {f'item_{i+1}': {'text': items[i], 'score': f"{scores[i]:.2%}"} for i in range(4)}
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/evaluar', methods=['POST'])
def evaluar_estudiante():
    try:
        datos = request.form
        nombre = datos.get('nombre')
        respuestas = datos.get('respuestas', '')

        # Validar que la respuesta esté dentro del ámbito de Cálculo I
        if not is_allowed_topic(respuestas):
            # Mensaje claro para el estudiante
            return jsonify({
                'error': 'Por favor envía solo respuestas relacionadas con Cálculo I (ej.: límites, derivadas, integrales, inecuaciones, proposiciones, funciones).'
            }), 400

        resultado = call_ai_api(respuestas)

        # Añadir nombre al resultado para mayor claridad
        resultado['nombre'] = nombre

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    # Use 0.0.0.0 en desarrollo si quieres acceder desde otra máquina; por defecto queda en localhost
    app.run(debug=True)