"""
Descripción
===========
Módulo para procesar imágenes o documentos con Amazon Textract (OCR avanzado).

Permite extraer texto plano, pares clave-valor y tablas a partir de capturas, fotos o PDFs
usando el servicio Textract de AWS.

Funciones
===========
"""


import re
import boto3
from openai import OpenAI
import openai
from source.config_loader import get_aws_credentials, get_openai_key

def corregir_ortografia(texto, model="gpt-4"):
    """
    Corrige ortografía y redacción en español utilizando OpenAI GPT-4.

    Parameters
    ----------
    texto : str
        Texto limpio y anonimizado a corregir.
    model : str
        Modelo de OpenAI (por defecto: "gpt-4").

    Returns
    -------
    str
        Texto corregido en redacción y ortografía.
    """
    client = OpenAI(api_key=get_openai_key())

    prompt = (
        "Corrige ortografía y redacción del siguiente mensaje en español. "
        "No inventes información ni quites contenido relevante. "
        "Solo corrige los errores:\n\n"
        f"{texto}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un corrector ortográfico profesional."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

def extraer_texto_textract(documento):
    """
    Extrae texto plano desde un archivo (imagen o PDF) usando Amazon Textract.

    Esta función se conecta al servicio Textract de AWS utilizando credenciales
    proporcionadas desde un archivo de configuración. Puede manejar archivos 
    locales (ruta como string) o archivos en memoria (bytes).

    Parameters
    ----------
    documento : str or bytes
        Ruta al archivo en disco (por ejemplo, 'solicitud.pdf' o 'img.png'), 
        o contenido binario en memoria, como el que devuelve uploaded_file.read() en Streamlit.

    Returns
    -------
    str
        Texto concatenado línea por línea, extraído por Textract a partir del documento.

    Raises
    ------
    TypeError
        Si el argumento 'documento' no es ni una ruta válida (str) ni un objeto binario (bytes).
    """
    access_key, secret_key, region = get_aws_credentials()
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    textract = session.client("textract")

    if isinstance(documento, str):
        with open(documento, "rb") as f:
            content = f.read()
    elif isinstance(documento, bytes):
        content = documento
    else:
        raise TypeError("El argumento 'documento' debe ser una ruta (str) o contenido binario (bytes).")

    response = textract.detect_document_text(Document={'Bytes': content})
    bloques = response.get("Blocks", [])
    lineas = [b["Text"] for b in bloques if b["BlockType"] == "LINE"]
    return "\n".join(lineas)

def extraer_origen_y_titulo(texto):
    """
    Extrae el origen (etiqueta entre corchetes) y el título del correo a partir del texto OCR.

    Esta función busca en el texto la primera línea que contenga un patrón tipo:
    "[ORIGEN] título del mensaje", como suele encontrarse en encabezados de correos institucionales.
    Si no encuentra coincidencias, devuelve valores por defecto.

    Parameters
    ----------
    texto : str
        Texto completo extraído por OCR, que incluye encabezado y cuerpo del correo.

    Returns
    -------
    tuple of str
        Una tupla con dos elementos:
        - origen : str
            Etiqueta extraída entre corchetes (por ejemplo, "TRANSPARENCIA").
        - titulo : str
            Texto que sigue a la etiqueta, considerado como el título del mensaje.
            Si no se detecta patrón, ambos valores serán: ("Desconocido", "Sin título detectado").
    """
    for linea in texto.split("\n"):
        match = re.search(r"\[(.*?)\]\s*(.+)", linea)
        if match:
            origen = match.group(1).strip()
            titulo = match.group(2).strip()
            return origen, titulo
    return "Desconocido", "Sin título detectado"

def limpiar_y_anonimizar(texto, origen=None, titulo=None):
    """
    Limpia el texto extraído por OCR eliminando ruido visual, datos personales, encabezados duplicados
    y metadatos de interfaces de correo.

    Esta función realiza una serie de transformaciones para mejorar la calidad del texto antes de pasarlo
    al modelo de corrección ortográfica. Entre otras cosas, elimina:
    - Nombres y saludos comunes
    - Correos electrónicos, reemplazándolos por [correo]
    - Encabezados de correo repetidos (extraídos como origen y título)
    - Frases comunes de interfaz (e.g. "Responder", "Reenviar", "Bloquear remitente")
    - Fechas, horarios y palabras muy cortas (ruido típico del OCR)

    Parameters
    ----------
    texto : str
        Texto plano extraído por OCR.
    origen : str, optional
        Origen del mensaje extraído del encabezado (entre corchetes). Se usa para eliminar el encabezado redundante.
    titulo : str, optional
        Título extraído del mensaje. Se usa junto con `origen` para eliminar encabezado duplicado.

    Returns
    -------
    str
        Texto limpio y anonimizado, sin metadatos visuales, nombres ni formatos de correo electrónico.
    """
    texto = re.sub(r"(?i)(atte:|saludos cordiales|gracias|juan p[ée]rez|mar[íi]a ram[íi]rez|jose gonz[aá]lez)", "", texto)
    texto = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[correo]", texto)

    if origen and titulo:
        encabezado = f"[{origen}] {titulo}"
        texto = texto.replace(encabezado, "")

    texto = re.sub(r"(?i)^(responder|reenviar)$", "", texto, flags=re.MULTILINE)

    patrones_ruido = [
        r"<\[correo\]>",
        r"(?i)para:",
        r"(?i)este remitente.*no pertenece",
        r"\bsáb\b|\blun\b|\bmar\b|\bmié\b|\bjue\b|\bvie\b|\bsab\b",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{1,2}:\d{2} (AM|PM)",
        r"(?i)bloquear remitente"
    ]

    lineas = texto.splitlines()
    lineas_filtradas = []
    for linea in lineas:
        if len(linea.strip()) <= 2:
            continue
        if any(re.search(pat, linea) for pat in patrones_ruido):
            continue
        lineas_filtradas.append(linea)

    texto_limpio = " ".join(lineas_filtradas)
    texto_limpio = re.sub(r"\s{2,}", " ", texto_limpio)
    return texto_limpio.strip()

def generar_json_desde_correo(texto_ocr):
    """
    Genera un diccionario JSON estructurado a partir del texto extraído por OCR de una imagen o PDF.

    Esta función:
    - Extrae el origen y el título del correo desde la primera línea con formato [ORIGEN] TÍTULO.
    - Limpia el texto eliminando ruido visual, encabezados redundantes, correos y metadatos innecesarios.
    - Corrige ortografía y redacción del mensaje completo utilizando un modelo LLM (GPT-4).
    - Devuelve un diccionario estructurado con los tres campos principales del mensaje.

    Parameters
    ----------
    texto_ocr : str
        Texto crudo extraído por OCR (usualmente desde Amazon Textract).

    Returns
    -------
    dict
        Diccionario con los siguientes campos:
        - "origen": etiqueta entre corchetes que indica la fuente de la solicitud (por ejemplo, "TRANSPARENCIA").
        - "titulo": texto que acompaña al origen, sirve como resumen o asunto de la solicitud.
        - "mensaje": cuerpo del mensaje corregido en ortografía y redacción.
    """
    origen, titulo = extraer_origen_y_titulo(texto_ocr)
    cuerpo_limpio = limpiar_y_anonimizar(texto_ocr, origen, titulo)
    cuerpo_corregido = corregir_ortografia(cuerpo_limpio)
    return {
        "origen": origen,
        "titulo": titulo,
        "mensaje": cuerpo_corregido
    }
