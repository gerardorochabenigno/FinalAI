"""
Descripción
===========

Este módulo carga la configuración de credenciales y parámetros desde un archivo YAML,
y valida que estén presentes los campos necesarios para conectarse a servicios externos
como AWS y OpenAI.

Funciones

"""

import yaml
import os

CONFIG_PATH = "config/config.yaml"


def cargar_config(path=CONFIG_PATH):
    """
    Carga la configuración desde un archivo YAML.
    Parameters
    ----------
    path : str
        Ruta al archivo de configuración (por defecto: "config/config.yaml").
    
    Returns
    -------
    dict
        Diccionario con la configuración cargada.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_aws_credentials():
    """
    Obtiene las credenciales necesarias para conectarse a los servicios de AWS desde un archivo de configuración local.

    Esta función carga y valida que estén presentes las siguientes claves en el archivo `config.yaml`:
    - access_key_id
    - secret_access_key
    - region

    Si alguna de ellas no está definida, se lanza una excepción.

    Returns
    -------
    tuple of str
        Una tupla con tres elementos:
        - access_key_id : str
        - secret_access_key : str
        - region : str

    Raises
    ------
    ValueError
        Si alguna de las claves necesarias no se encuentra en la sección 'aws' del archivo de configuración.
    """
    
    config = cargar_config()
    aws = config.get("aws", {})

    if not all(k in aws for k in ("access_key_id", "secret_access_key", "region")):
        raise ValueError("Faltan credenciales de AWS en config.yaml")

    return aws["access_key_id"], aws["secret_access_key"], aws["region"]


def get_openai_key():
    config = cargar_config()
    openai_conf = config.get("openai", {})

    if "api_key" not in openai_conf:
        raise ValueError("Falta la clave de OpenAI en config.yaml")

    return openai_conf["api_key"]
