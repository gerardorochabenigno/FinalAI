import requests
from bs4 import BeautifulSoup
import os
import re
from PyPDF2 import PdfReader

# Crear carpetas
os.makedirs('normatividad_completo', exist_ok=True)
os.makedirs('normatividad_compilado', exist_ok=True)

# URL de la página principal
url = 'https://www.banxico.org.mx/marco-normativo/normativa-agrupada-por-sujeto.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

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
                pdf_path = os.path.join('normatividad_completo', pdf_name)

                # Descargar PDF
                pdf_response = requests.get(pdf_url)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f'Descargado: {pdf_name}')

                # Leer PDF para ver si contiene "texto compilado"
                try:
                    reader = PdfReader(pdf_path)
                    text = ""
                    for page in reader.pages[:2]:  # solo lee las primeras páginas para acelerar
                        text += page.extract_text() or ""

                    if 'texto compilado' in text.lower():
                        dest_path = os.path.join('normatividad_compilado', pdf_name)
                        os.rename(pdf_path, dest_path)
                        print(f"Conservado (texto compilado): {pdf_name}")
                    else:
                        os.remove(pdf_path)
                        print(f"Eliminado: {pdf_name}")
                except Exception as e:
                    print(f"⚠ Error leyendo {pdf_name}: {e}")
