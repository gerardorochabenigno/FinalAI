"""
Descripción
===========
Este módulo automatiza la descarga de documentos regulatorios agrupados por sujeto,
y filtra únicamente aquellos que contienen la expresión 'texto compilado' en su contenido,
preservando únicamente los documentos relevantes para análisis normativo.

Funciones
===========

"""

import requests
from bs4 import BeautifulSoup
import os
import re
from PyPDF2 import PdfReader

def descargar_normatividad_compilada(destino='normatividad_compilado', carpeta_temp='normatividad_completo'):
    """
    Descarga los documentos de normatividad desde la página de Banxico y conserva solo aquellos que contienen 'texto compilado'.
    El texto compilado contiene la versión más reciente de la normatividad, por lo que es importante conservarlo.
    Los demás documentos no nos interesan porque contienen texto repetido o que ya no es relevante debido a que puede haber que ya no son vigentes.

    Params
    ----------
    destino : str
        Carpeta donde se guardarán los PDFs con texto compilado.
    carpeta_temp : str
        Carpeta temporal donde se descargan todos los PDFs antes de filtrar.

    Returns
    -------
    list[str]
        Lista de archivos que fueron conservados como 'texto compilado'.
    """

    # Verificamos que las carpetas de destino y temporal existen y si no, las creamos
    if not os.path.exists(destino):
        os.makedirs(destino, exist_ok=True)
    if not os.path.exists(carpeta_temp):
        os.makedirs(carpeta_temp, exist_ok=True)

    url = 'https://www.banxico.org.mx/marco-normativo/normativa-agrupada-por-sujeto.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conservados = []

    for link in soup.find_all('a', href=True):
        href = 'https://www.banxico.org.mx' + link['href']
        
        if href.lower().endswith('html'):
            response_norm = requests.get(href)
            soup_norm = BeautifulSoup(response_norm.text, 'html.parser')

            for link_norm in soup_norm.find_all('a', href=True):
                href_norm = link_norm['href']
                if href_norm.lower().endswith('.pdf'):
                    pdf_url = href_norm if href_norm.startswith('https') else f'https://www.banxico.org.mx{href_norm}'
                    pdf_name = pdf_url.split('/')[-1]
                    pdf_path = os.path.join(carpeta_temp, pdf_name)

                    try:
                        pdf_response = requests.get(pdf_url)
                        with open(pdf_path, 'wb') as f:
                            f.write(pdf_response.content)
                        print(f'Descargado: {pdf_name}')

                        reader = PdfReader(pdf_path)
                        text = ""
                        for page in reader.pages[:2]:
                            text += page.extract_text() or ""

                        if 'texto compilado' in text.lower():
                            dest_path = os.path.join(destino, pdf_name)
                            os.rename(pdf_path, dest_path)
                            print(f"✅ Conservado: {pdf_name}")
                            conservados.append(dest_path)
                        else:
                            os.remove(pdf_path)
                            print(f"🗑️ Eliminado: {pdf_name}")

                    except Exception as e:
                        print(f"⚠️ Error procesando {pdf_name}: {e}")

    return conservados