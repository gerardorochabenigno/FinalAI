import os
import pymupdf
import pdfplumber
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import warnings
warnings.filterwarnings("ignore")

CARPETA_PDFS = "normatividad_compilado"

# Inicializar ChromaDB
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./chroma_data")
nombre_coleccion = "normatividad"
if nombre_coleccion in [c.name for c in chroma_client.list_collections()]:
    chroma_client.delete_collection(nombre_coleccion)

collection = chroma_client.create_collection(
    name=nombre_coleccion,
    embedding_function=embedding_fn
)

# Función para convertir tabla a texto legible
def tabla_a_texto(tabla):
    texto = []
    encabezados = tabla[0]
    for fila in tabla[1:]:
        celdas = [f"{encabezados[i]}: {celda}" for i, celda in enumerate(fila) if i < len(encabezados)]
        texto.append("; ".join(celdas))
    return "\n".join(texto)

# Función combinada para extraer texto y tablas
def extraer_con_tablas(ruta_pdf):
    texto_total = []
    doc = pymupdf.open(ruta_pdf)  # solo lo abrimos una vez
    with pdfplumber.open(ruta_pdf) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tablas = page.extract_tables()
            if tablas and len(tablas[0]) > 1:
                for tabla in tablas:
                    texto_total.append(tabla_a_texto(tabla))
            else:
                texto_total.append(doc[page_num].get_text())
    return "\n\n".join(texto_total)

# Indexación
for archivo in os.listdir(CARPETA_PDFS):
    if archivo.endswith(".pdf"):
        ruta = os.path.join(CARPETA_PDFS, archivo)
        print(f"📄 Procesando: {archivo}")
        texto = extraer_con_tablas(ruta)
        chunks = [p.strip() for p in texto.split("\n\n") if len(p.strip()) > 100]
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                ids=[f"{archivo}_{i}"],
                metadatas=[{"source": archivo}]
            )

print("✅ Documentos indexados con tablas y texto en ChromaDB.")