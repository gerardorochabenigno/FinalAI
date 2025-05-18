from source.rag_utils import consultar_contexto_rag, normalizar_fuentes, generar_respuesta_con_contexto

import json

# Ruta al archivo JSON generado por el OCR
ruta_json = "output/ej1.json"

# Cargar el JSON desde disco
with open(ruta_json, "r", encoding="utf-8") as f:
    json_data = json.load(f)

mensaje = json_data["mensaje"]

contexto, fuentes = consultar_contexto_rag(mensaje)
print("\nContexto normativo relevante:\n")
print(len(fuentes))
print(normalizar_fuentes(fuentes))