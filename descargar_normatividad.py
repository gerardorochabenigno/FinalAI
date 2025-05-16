import requests
from bs4 import BeautifulSoup
import os

# URL de la página de normatividad
url = 'https://www.banxico.org.mx/marco-normativo/normativa-agrupada-por-sujeto.html'

# Realizar la solicitud HTTP
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Crear directorio para guardar los PDFs
os.makedirs('normatividad', exist_ok=True)

# Buscar todos los enlaces a PDFs
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.lower().endswith('.pdf'):
        pdf_url = href if href.startswith('http') else f'https://www.banxico.org.mx{href}'
        pdf_name = pdf_url.split('/')[-1]
        pdf_path = os.path.join('normatividad_pdf', pdf_name)
        
        # Descargar el PDF
        pdf_response = requests.get(pdf_url)
        with open(pdf_path, 'wb') as f:
            f.write(pdf_response.content)
        print(f'Descargado: {pdf_name}')
