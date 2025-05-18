"""
# Proyecto Final de Agentes de Inteligencia Artificial, Instituto Tecnológico Autónomo de México (ITAM), Primavera 2025

**Nombre: Gerardo Rocha Benigno (219932)**

**Clave:  219932**

Bienvenido a la documentación de los modulos del proyecto **Procesador OCR de Solicitudes Normativas y Generador de Respuestas**.

Este sistema permite:

-  Recibir solicitudes de transparencia en formato imagen
-  Aplicar OCR con Amazon Textract
-  Limpiar y anonimizar el texto automáticamente
-  Consultar normatividad relevante con RAG (ChromaDB + GPT)
-  Generar respuestas en lenguaje formal, profesional y basado en evidencia normativa

---

**Estructura del sistema**

- `chroma_utils.py`: manejo de la base de datos ChromaDB
- `config_loader.py`: manejo seguro de credenciales
- `ocr_utils.py`: procesamiento de imagen y limpieza de texto
- `rag_utils.py`: recuperación de normativa y generación de respuestas
- `web_utils.py`: generación de base de datos de normativa

"""

# source/__init__.py