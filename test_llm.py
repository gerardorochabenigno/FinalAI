import json
from source.rag_utils import responder_desde_json

# Ruta al archivo JSON generado por el OCR
ruta_json = "output/ej1.json"

# Cargar el JSON desde disco
with open(ruta_json, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Generar respuesta con RAG + LLM
respuesta = responder_desde_json(json_data)

# Mostrar en consola
print("\nRespuesta generada:\n")
print(respuesta)