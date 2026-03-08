from model import conversor as ConversorModel
from shared.constantes import MONEDAS_VALIDAS
# ─────────────────────────────────────────────
#  Instancia única del modelo (Singleton)
# ─────────────────────────────────────────────
_modeloConversor = ConversorModel.conversor()



# ─────────────────────────────────────────────
#  Convertir monto entre monedas
# ─────────────────────────────────────────────
def convertir(monto: float, moneda_origen: str, moneda_destino: str) -> float | str:
    """
    Convierte un monto de moneda_origen a moneda_destino.
    Retorna el float convertido, o un string con el error si algo falla.
    """
    if moneda_origen not in MONEDAS_VALIDAS:
        return f"Moneda origen '{moneda_origen}' no es válida."
    if moneda_destino not in MONEDAS_VALIDAS:
        return f"Moneda destino '{moneda_destino}' no es válida."
    if not isinstance(monto, (int, float)) or monto < 0:
        return "El monto debe ser un número positivo."

    try:
        return _modeloConversor.convertir(monto, moneda_origen, moneda_destino)
    except Exception as e:
        return f"Error en conversión: {e}"





# ─────────────────────────────────────────────
#  Obtener tasas de referencia
# ─────────────────────────────────────────────
def obtenerTasas() -> dict:
    """Retorna el dict de tasas actuales {moneda: valor_en_CRC}."""
    return _modeloConversor.obtenerTasas()
