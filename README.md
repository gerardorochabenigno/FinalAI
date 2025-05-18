# Agentes de Inteligencia Artificial: Trabajo Final - Gerardo Rocha Benigno (219932)

# Procesador OCR de Solicitudes Normativas y Generador de Respuestas.

## Objetivo del Proyecto

Desarrollar un asistente automatizado que recibe imágenes de solicitudes (fotos o screenshots), extrae su contenido con OCR, lo limpia y corrige, y genera una respuesta profesional basada en la normatividad del Banco de México utilizando técnicas de recuperación aumentada por generación (RAG).

## Metodología

Mediante una interfaz interactiva en Streamlit, el usuario puede cargar una imagen con la solicitud que requiera y el sistema realiza los siguientes pasos:

1. Aplica OCR avanzado para extraer el texto utilizando Amazon textract y un LLM (GPT) para generar un archivo utilizable en formato JSON, limpio y eliminando información sensible y datos personales.
2. Busca fragmentos normativos relevantes en una base vectorial (ChromaDB).
3. Genera una respuesta con lenguaje natural mediante un modelo LLM (GPT) y RAG (ChromaDB).

---

## Casos de uso

- Simula el trabajo de una **ventanilla de transparencia** y de un **equipo de compliance**.
- Atiende solicitudes ciudadanas o institucionales.
---

## Tecnologías utilizadas

-  **Amazon Textract** como herramienta principal de OCR robusto (extrae texto, tablas y campos clave desde imágenes o PDFs)
-  `ChromaDB` + `sentence-transformers` para recuperación semántica (RAG)
-  `OpenAI GPT-4` para generación de respuestas normativas en lenguaje natural
-  `pdfplumber` para extracción precisa de tablas desde documentos regulatorios
-  **Exportación estructurada** en `JSON`, `CSV` y `PDF` para integración institucional
-  **Interfaz interactiva** desarrollada en `Streamlit`

---

##  Estructura del proyecto
```bash
├── config/
│   └── config.yaml           # Credenciales y parámetros del sistema
├── docs/                     # Documentación generada con pdoc
├── ejemplos_ocr/             # Ejemplos de imágenes de solicitudes
├── metadara/                 # Metadatos de normatividad
├── normatividad_compilado/   # PDFs de normatividad de Banco de México
├── output/                   # Carpeta que almacena JSONs generados con OCR
├── source/
│   ├── chroma_utils.py       # Funciones para indexar archivos PDF en ChromaDB
│   ├── config_loader.py      # Funciones para cargar configuración y clientes
│   ├── ocr_utils.py          # Funciones para realizar OCR con Amazon Textract y generar JSON
│   ├── rag_utils.py          # Funciones para realizar búsqueda semántica en ChromaDB y generar respuestas
│   ├── web_utils.py          # Funciones para descargar normatividad desde la página de Banco de México
├── normatividad_compilado/   # PDFs de normatividad de Banco de México
├── chroma_data/              # Persistencia local de la base vectorial de normaividad
├── output/                   # Carpeta que almacena JSONs generados con OCR
└── README.md                 # Este archivo    
├── app.py                    # App principal en Streamlit
├── base_normatividad_chroma.py # Script para crear la base de datos de normatividad en ChromaDB
├── descargar_normatividad.py  # Script para descargar normatividad de Banco de México
```

## Instalación

- 1. Para ejecutar el proyecto, asegúrate de tener instaladas las dependencias necesarias. Puedes hacerlo ejecutando el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt
```
- 2. Asegúrate de tener las credenciales de Amazon Textract y OpenAI configuradas en el archivo `config/config.yaml`. En la carpeta `config`, crea un archivo llamado `config_template.yaml` que te puede servir de base.

- 3. Ejecuta los scripts `descargar_normatividad.py` y `base_normatividad_chroma.py` para descargar la normatividad de Banco de México y crear la base de datos de normatividad en ChromaDB. Puedes hacerlo ejecutando los siguientes comandos en tu terminal (esto tarda algunos minutos):

```bash
python3 descargar_normatividad.py
python3 base_normatividad_chroma.py
```

- 4. Inicia la aplicación de Streamlit:

```bash
streamlit run app.py
```

- 5. Listo! Ahora puedes cargar imágenes de solicitudes y recibir respuestas generadas automáticamente.


## Documentación
La documentación de las funciones creadas y almacenadas en la carpeta `source` para este proyecto se genera automáticamente utilizando `pdoc` y se encuentra en la carpeta `docs_html`. Para abrir la documentación en tu navegador, da clic aquí: [Documentación del proyecto](https://gerardorochabenigno.github.io/FinalAI/source.html)

