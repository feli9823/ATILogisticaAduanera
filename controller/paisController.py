from model import pais as PaisModel
from validation import paisValidador

# ─────────────────────────────────────────────
#  Instancia única del modelo (Singleton)
# ─────────────────────────────────────────────
_modeloPais = PaisModel.pais()


# ─────────────────────────────────────────────
#  Guardar país (RF-10)
# ─────────────────────────────────────────────
def guardarPais(nombre: str, tarifaImpuesto: float, tipoMoneda: str) -> dict | str:
    """
    Valida y guarda un nuevo país.
    Retorna el país creado como dict si tuvo éxito,
    o un string con el mensaje de error si falló.
    """
    if not paisValidador.validarNombre(nombre):
        return "El nombre del país no es válido. Solo se permiten letras, espacios y guiones."
    if not paisValidador.validarTarifa(tarifaImpuesto):
        return "La tarifa de impuesto debe ser un número entre 0 y 100."
    if not paisValidador.validarMoneda(tipoMoneda):
        return "La moneda seleccionada no es válida."

    exito = _modeloPais.agregarPais(nombre, tarifaImpuesto, tipoMoneda)
    if not exito:
        return "No se pudo guardar el país. Intenta de nuevo."

    nuevoId = max(_modeloPais.listaPais.keys(), default=0)
    return {
        "id"             : nuevoId,
        "nombre"         : nombre,
        "tarifaImpuesto" : tarifaImpuesto,
        "tipoMoneda"     : tipoMoneda,
    }


# ─────────────────────────────────────────────
#  Modificar país
# ─────────────────────────────────────────────
def modificarPais(id: int, nombre: str = None, tarifaImpuesto: float = None, tipoMoneda: str = None) -> bool | str:
    """
    Modifica un país existente por id.
    Retorna True si se modificó,
    o un string con el mensaje de error si falló.
    """
    if id not in _modeloPais.listaPais:
        return "El país que intentás modificar no existe."
    if nombre is not None and not paisValidador.validarNombre(nombre):
        return "El nombre del país no es válido. Solo se permiten letras, espacios y guiones."
    if tarifaImpuesto is not None and not paisValidador.validarTarifa(tarifaImpuesto):
        return "La tarifa de impuesto debe ser un número entre 0 y 100."
    if tipoMoneda is not None and not paisValidador.validarMoneda(tipoMoneda):
        return "La moneda seleccionada no es válida."

    _modeloPais.modificarPais(id, nombre=nombre, tarifaImpuesto=tarifaImpuesto, tipoMoneda=tipoMoneda)
    return True


# ─────────────────────────────────────────────
#  Eliminar país
# ─────────────────────────────────────────────
def eliminarPais(id: int) -> bool:
    """
    Elimina un país por id.
    Retorna True si se eliminó, False si no existía.
    """
    if id not in _modeloPais.listaPais:
        return False
    _modeloPais.eliminarPais(id)
    return True


# ─────────────────────────────────────────────
#  Obtener todos los países
# ─────────────────────────────────────────────
def obtenerPaises() -> list[dict]:
    """
    Retorna todos los países para mostrar en la tabla.
    Formato: [{"id": 1, "nombre": "...", "tarifaImpuesto": 0.0, "tipoMoneda": "USD"}, ...]
    """
    datos = _modeloPais.mostrarPais()
    return [
        {
            "id"             : id,
            "nombre"         : p["nombre"],
            "tarifaImpuesto" : p["tarifaImpuesto"],
            "tipoMoneda"     : p["tipoMoneda"],
        }
        for id, p in datos.items()
    ]


# ─────────────────────────────────────────────
#  Obtener país por id
# ─────────────────────────────────────────────
def obtenerPaisPorId(id: int) -> dict | None:
    datos = _modeloPais.listaPais
    if id in datos:
        return {"id": id, **datos[id]}
    return None