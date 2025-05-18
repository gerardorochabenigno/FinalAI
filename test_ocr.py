"""
Script: procesar_imagen.py

Este script toma una imagen (foto, escaneo o captura de un correo), aplica OCR usando Amazon Textract,
realiza limpieza visual, anonimiza, corrige ortografía con GPT-4 y guarda el resultado como JSON local.
"""

import os
import json
from source.ocr_utils import (
    extraer_texto_textract,
    generar_json_desde_correo
)



if __name__ == "__main__":
    ruta_imagen = "ejemplos_ocr/ej3.png"
    carpeta_salida = "output"
    os.makedirs(carpeta_salida, exist_ok=True)

    # ------------ Procesamiento ------------

    # 1. OCR
    texto_ocr = extraer_texto_textract(ruta_imagen)

    # 2. JSON estructurado limpio y corregido
    json_final = generar_json_desde_correo(texto_ocr)

    # 3. Guardar JSON localmente
    nombre_archivo = os.path.basename(ruta_imagen).replace(".png", ".json")
    ruta_json = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(json_final, f, indent=2, ensure_ascii=False)

    # 4. Confirmación
    print("\n✅ JSON generado y guardado en:", ruta_json)
    print("\nContenido:\n")
    print(json.dumps(json_final, indent=2, ensure_ascii=False))
