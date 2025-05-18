import streamlit as st
import os
import json
from source.ocr_utils import (
    extraer_texto_textract,
    generar_json_desde_correo
)
from source.rag_utils import responder_desde_json 

st.set_page_config(page_title="Procesador de Solicitudes", layout="centered")

st.title("Procesador de Solicitudes vía Imagen")
st.markdown("Sube una imagen o PDF con una solicitud de transparencia para extraer, limpiar y corregir el contenido.")

uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    st.info("Procesando...")

    # 1. Leer contenido
    content = uploaded_file.read()
    texto_ocr = extraer_texto_textract(content)

    # 2. Generar JSON
    json_final = generar_json_desde_correo(texto_ocr)

    # 3. Mostrar resultado
    st.success("Solicitud procesada correctamente")
    st.subheader("JSON generado:")
    st.json(json_final)

    # 4. Guardar JSON local
    nombre_archivo = uploaded_file.name.rsplit(".", 1)[0] + ".json"
    ruta_salida = os.path.join("output", nombre_archivo)
    os.makedirs("output", exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(json_final, f, indent=2, ensure_ascii=False)

    st.success(f"Archivo guardado en: `{ruta_salida}`")

    # 5. Descargar JSON
    st.download_button(
        label="Descargar JSON",
        data=json.dumps(json_final, indent=2, ensure_ascii=False),
        file_name=nombre_archivo,
        mime="application/json"
    )

    # 6.
    if st.button("Generar respuesta normativa con GPT"):
        with st.spinner("Consultando normatividad y generando respuesta..."):
            respuesta = responder_desde_json(json_final)

        st.subheader("Respuesta generada:")
        st.write(respuesta)

        # 7. Descargar respuesta como .txt
        nombre_txt = nombre_archivo.replace(".json", "_respuesta.txt")
        st.download_button(
            label="Descargar respuesta en .txt",
            data=respuesta,
            file_name=nombre_txt,
            mime="text/plain"
        )