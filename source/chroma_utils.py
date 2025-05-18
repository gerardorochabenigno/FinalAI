"""
Descripción
===========

Este modulo contiene funciones para extraer texto y tablas de documentos PDF. Las tablas se convierten 
en texto legible con formato "columna: valor", y todo el contenido es dividido en fragmentos 
que se almacenan como embeddings en una colección de ChromaDB.

Funciones
===========

"""

import os
import pymupdf
import pdfplumber
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import warnings
warnings.filterwarnings("ignore")

def tabla_a_texto(tabla):
    """
    Convierte una tabla extraída de un PDF en texto legible tipo "columna: valor".

    Parameters
    ----------
    tabla : list[list[str]]
        Lista de listas que representa una tabla extraída con pdfplumber.
        La primera sublista debe contener los encabezados.

    Returns
    -------
    str
        Texto formateado de la tabla con pares "encabezado: valor", una fila por línea.
    """

    texto = []
    encabezados = tabla[0]
    for fila in tabla[1:]:
        celdas = [f"{encabezados[i]}: {celda}" for i, celda in enumerate(fila) if i < len(encabezados)]
        texto.append("; ".join(celdas))
    return "\n".join(texto)

def extraer_con_tablas(ruta_pdf):
    """
    Extrae contenido textual y tabular de un archivo PDF combinando pdfplumber y pymupdf.

    La función recorre cada página del PDF especificado. Si la página contiene una tabla
    con más de una fila (para evitar tablas vacías o mal formateadas), esta se transforma 
    en un bloque de texto legible tipo "columna: valor" mediante la función `tabla_a_texto()`.
    Si no se detectan tablas, se extrae el texto plano de la página usando pymupdf.

    Parameters
    ----------
    ruta_pdf : str
        Ruta al archivo PDF que se desea procesar.

    Returns
    -------
    str
        Texto completo del documento, incluyendo tanto texto plano como
        representaciones legibles de tablas, separado por saltos dobles de línea.
    """
    texto_total = []
    doc = pymupdf.open(ruta_pdf)
    with pdfplumber.open(ruta_pdf) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tablas = page.extract_tables()
            if tablas and len(tablas[0]) > 1:
                for tabla in tablas:
                    texto_total.append(tabla_a_texto(tabla))
            else:
                texto_total.append(doc[page_num].get_text())
    return "\n\n".join(texto_total)

def indexar_pdfs_en_chroma(carpeta_pdfs="normatividad_compilado", path_chroma="./chroma_data", nombre_coleccion="normatividad"):
    """
    Indexa documentos PDF en una colección ChromaDB con embeddings de texto.

    Parameters
    ----------
    carpeta_pdfs : str
        Ruta a la carpeta con archivos PDF a indexar.
    path_chroma : str
        Ruta al almacenamiento persistente de ChromaDB.
    nombre_coleccion : str
        Nombre de la colección ChromaDB que se va a crear.

    Returns
    -------
    None
    """

    if not os.path.exists(carpeta_pdfs):
        raise FileNotFoundError(f"La carpeta '{carpeta_pdfs}' no existe.")

    embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    chroma_client = chromadb.PersistentClient(path=path_chroma)

    if nombre_coleccion in [c.name for c in chroma_client.list_collections()]:
        chroma_client.delete_collection(nombre_coleccion)

    collection = chroma_client.create_collection(
        name=nombre_coleccion,
        embedding_function=embedding_fn
    )

    for archivo in os.listdir(carpeta_pdfs):
        if archivo.lower().endswith(".pdf"):
            ruta = os.path.join(carpeta_pdfs, archivo)
            print(f"📄 Procesando: {archivo}")
            texto = extraer_con_tablas(ruta)
            chunks = [p.strip() for p in texto.split("\n\n") if len(p.strip()) > 100]
            for i, chunk in enumerate(chunks):
                collection.add(
                    documents=[chunk],
                    ids=[f"{archivo}_{i}"],
                    metadatas=[{"source": archivo}]
                )

    print(f"✅ Documentos indexados en colección '{nombre_coleccion}'.")