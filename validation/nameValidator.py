
import re


def validarNombre(nombre: str) -> bool:
    if not isinstance(nombre, str) or not nombre.strip():
        return False
    # Acepta letras (incluyendo tildes y ñ), espacios y guiones
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$", nombre.strip()):
        return False
    return True 