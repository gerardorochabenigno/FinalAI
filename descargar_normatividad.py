from source.web_utils import descargar_normatividad_compilada

if __name__ == "__main__":
    archivos_conservados = descargar_normatividad_compilada()
    print(f"\nTotal de documentos conservados: {len(archivos_conservados)}")