"""
Descripción
===========

Este módulo se encarga de:
- Consultar una colección ChromaDB con embeddings de fragmentos normativos de Banco de México
- Recuperar fragmentos normativos relevantes
- Generar una respuesta con LLM (GPT-4) basada en el contexto y metadatos
- Formatear la respuesta de forma institucional usando un catálogo de nombres legibles

Funciones
==========
"""

import chromadb
from openai import OpenAI
import os
import re
import json
from source.config_loader import get_openai_key
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Inicializar cliente de OpenAI
client = OpenAI(api_key=get_openai_key())

# Inicializar cliente de ChromaDB y cargar colección
chroma_client = chromadb.PersistentClient(path="chroma_data")
coleccion = chroma_client.get_collection("normatividad")

# Cargar catálogo de nombres legibles
with open("metadata/catalogo_normatividad.json", "r", encoding="utf-8") as f:
    CATALOGO_NORMAS = json.load(f)

def consultar_contexto_rag(mensaje_usuario, k=10):
    """
    Recupera los fragmentos más relevantes desde ChromaDB y extrae fuentes normativas.

    Parameters
    ----------
    mensaje_usuario : str
        Pregunta del usuario corregida y limpia.
    k : int
        Número de fragmentos a recuperar.

    Returns
    -------
    tuple (contexto:str, fuentes:set)
        Texto combinado de fragmentos relevantes y conjunto de nombres de normativas (source).
    """
    resultados = coleccion.query(
        query_texts=[mensaje_usuario],
        n_results=k
    )
    documentos = resultados["documents"][0]
    metadatos = resultados["metadatas"][0]
    fuentes = set(md.get("source", "Desconocido") for md in metadatos)
    contexto = "\n\n".join(documentos)
    return contexto, fuentes

def normalizar_fuentes(fuentes):
    """
    Reemplaza los nombres de archivo por títulos legibles usando el catálogo.

    Parameters
    ----------
    fuentes : set
        Conjunto de nombres de archivo PDF

    Returns
    -------
    list[str]
        Lista de nombres legibles de normatividad
    """
    return [CATALOGO_NORMAS.get(f, f) for f in sorted(fuentes)]

def generar_respuesta_con_contexto(mensaje_usuario, contexto, fuentes, model="gpt-3.5-turbo"):
    """
    Genera una respuesta normativa profesional basada en los fragmentos recuperados y fuentes legales.

    Parameters
    ----------
    mensaje_usuario : str
        Solicitud del usuario (ya corregida).
    contexto : str
        Texto combinado de fragmentos normativos.
    fuentes : set
        Conjunto de nombres de normativas (archivo fuente).
    model : str
        Modelo de lenguaje a utilizar (por defecto: gpt-3.5-turbo).

    Returns
    -------
    str
        Respuesta generada por el modelo en estilo institucional.
    """
    nombres_legibles = normalizar_fuentes(fuentes)
    lista_normas = "\n".join(f"- {n}" for n in nombres_legibles)

    prompt = f"""
    Eres un asistente normativo formal, preciso y respetuoso. Tu tarea es responder a solicitudes de información
    utilizando exclusivamente el contexto normativo proporcionado. No inventes normativas ni procedimientos.

    Las siguientes normativas fueron identificadas como relevantes por el sistema de recuperación semántica. 
    Inclúyelas explícitamente en tu respuesta si las utilizas para fundamentar tu argumento:

    {lista_normas}

    ---

    Fragmentos normativos relevantes:
    {contexto}

    ---

    Solicitud del ciudadano:
    {mensaje_usuario}

    ---

    Redacta una respuesta profesional y normativa, citando al menos una de las normativas mencionadas si su contenido es utilizado.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()

def responder_desde_json(json_correo):
    """
    Flujo completo: dado un JSON generado por el OCR, recupera contexto y genera la respuesta.

    Parameters
    ----------
    json_correo : dict
        Diccionario con las claves: 'origen', 'titulo', 'mensaje'

    Returns
    -------
    str
        Respuesta normativa completa generada con ayuda de contexto.
    """
    mensaje = json_correo["mensaje"]
    contexto, fuentes = consultar_contexto_rag(mensaje)
    respuesta = generar_respuesta_con_contexto(mensaje, contexto, fuentes)
    return respuesta