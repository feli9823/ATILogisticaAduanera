def validarProductoId(productoId) -> bool:
    return isinstance(productoId, int) and productoId > 0

def validarPaisId(paisId) -> bool:
    return isinstance(paisId, int) and paisId > 0

def validarPrecioModificado(precio) -> bool:
    try:
        precio = float(precio)
        if precio < 0:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validarMoneda(moneda: str) -> bool:
    MONEDAS_VALIDAS = {"CRC", "USD", "EUR", "BRL"}
    return isinstance(moneda, str) and moneda.strip() in MONEDAS_VALIDAS
