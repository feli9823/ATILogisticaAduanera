import re
def validarNombre(nombre: str) -> bool:
    if not isinstance(nombre, str) or not nombre.strip():
        return False
    # Acepta letras (incluyendo tildes y ñ), espacios y guiones
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$", nombre.strip()):
        return False
    return True 

def validarTarifa(tarifa: float) -> bool:
    return isinstance(tarifa, (int, float)) and 0 <= tarifa <= 100

MONEDAS_VALIDAS = {"CRC", "USD", "EUR", "BRL"}

def validarMoneda(moneda: str) -> bool:
    return isinstance(moneda, str) and moneda.strip() in MONEDAS_VALIDAS