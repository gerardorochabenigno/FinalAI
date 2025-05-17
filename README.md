# Agentes de Inteligencia Artificial: Trabajo Final

# 📄 Digitalizador y Analizador de Documentos

Este proyecto implementa un sistema inteligente para automatizar la atención a solicitudes de transparencia y de compliance. A partir de una imagen (foto, screenshot o escaneo) de una solicitud, el sistema:

1. Aplica OCR avanzado para extraer el texto.
2. Busca fragmentos normativos relevantes en una base vectorial (ChromaDB).
3. Genera una respuesta con lenguaje natural mediante un modelo LLM (GPT-4).
4. Exporta la respuesta en un chatbot y da la posibilidad de exportar la respuesta en formatos estructurados: JSON y PDF.

---

## 🚀 Casos de uso

- Simula el trabajo de una **ventanilla de transparencia** y de un **equipo de compliance**.
- Atiende solicitudes ciudadanas o institucionales.
- Revisa si ciertas prácticas cumplen o no con la normatividad vigente.
- Aplica OCR sobre fotos de correos, capturas de pantalla o documentos físicos.

---

## 🧠 Tecnologías utilizadas

- 🧠 `ChromaDB` + `sentence-transformers` para RAG
- 🤖 `OpenAI GPT-4` para generar respuestas en lenguaje natural
- ☁️ `Amazon Textract` (opcional) para OCR robusto desde AWS
- 🧪 `pdfplumber` para extracción de tablas en documentos normativos
- 📤 Exportación a `JSON`, `CSV` y `PDF`
- 💻 Interfaz en `Streamlit`

---

## 🗂️ Estructura del proyecto
```bash
├── app.py                    # App principal en Streamlit
├── config/
│   └── config.yaml           # Credenciales y parámetros del sistema
├── source/
│   ├── config_loader.py      # Funciones para cargar configuración y clientes
│   ├── llm_utils.py          # Llamadas a GPT-4 para generar respuestas
│   ├── ocr_utils.py          # OCR con preprocesamiento
│   ├── chroma_utils.py       # Indexación y búsqueda en ChromaDB
│   └── export_utils.py       # Funciones para guardar en JSON y PDF
├── normatividad_compilado/  # PDFs de normatividad
├── chroma_data/              # Persistencia local de la base vectorial
├── prompts/                  # Prompts usados por el LLM
├── output/                   # Carpeta para resultados generados
└── README.md