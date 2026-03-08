from shared.constantes import MONEDAS_VALIDAS
from validation.nameValidator import validarNombre

def validarTarifa(tarifa: float) -> bool:
    return isinstance(tarifa, (int, float)) and 0 <= tarifa <= 100


def validarMoneda(moneda: str) -> bool:
    return isinstance(moneda, str) and moneda.strip() in MONEDAS_VALIDAS