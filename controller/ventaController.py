from model import venta as VentaModel
from validation import ventaValidador
from controller import productosController, paisController

# ─────────────────────────────────────────────
#  Instancia única del modelo (Singleton)
# ─────────────────────────────────────────────
_modeloVenta = VentaModel.venta()


# ─────────────────────────────────────────────
#  Guardar venta
# ─────────────────────────────────────────────
def guardarVenta(productoId: int, paisId: int, precioModificado: float) -> dict | str:
    """
    Valida, resuelve nombres desde los controllers de producto y país,
    y guarda la venta.
    Retorna el dict de la venta creada, o un string con el error.
    """
    if not ventaValidador.validarProductoId(productoId):
        return "El producto seleccionado no es válido."
    if not ventaValidador.validarPaisId(paisId):
        return "El país seleccionado no es válido."
    if not ventaValidador.validarPrecioModificado(precioModificado):
        return "El precio debe ser un número positivo."

    # ── Resolver nombre y datos desde los controllers ────
    productos = productosController.obtenerProductos()
    producto  = next((p for p in productos if p["id"] == productoId), None)
    if not producto:
        return "El producto seleccionado no existe."

    paises = paisController.obtenerPaises()
    pais   = next((p for p in paises if p["id"] == paisId), None)
    if not pais:
        return "El país seleccionado no existe."

    if not ventaValidador.validarMoneda(pais["tipoMoneda"]):
        return "La moneda del país seleccionado no es válida."

    exito = _modeloVenta.agregarVenta(
        productoId       = productoId,
        nombreProducto   = producto["nombre"],
        paisId           = paisId,
        nombrePais       = pais["nombre"],
        moneda           = pais["tipoMoneda"],
        precioModificado = float(precioModificado),
    )
    if not exito:
        return "No se pudo guardar la venta. Intenta de nuevo."

    nuevoId = max(_modeloVenta.listaVentas.keys(), default=0)
    return {
        "id"              : nuevoId,
        "productoId"      : productoId,
        "nombreProducto"  : producto["nombre"],
        "paisId"          : paisId,
        "nombrePais"      : pais["nombre"],
        "moneda"          : pais["tipoMoneda"],
        "precioModificado": float(precioModificado),
    }


# ─────────────────────────────────────────────
#  Modificar venta
# ─────────────────────────────────────────────
def modificarVenta(id: int, productoId: int = None,
                   paisId: int = None, precioModificado: float = None) -> bool | str:
    """
    Modifica una venta existente por id.
    Retorna True si tuvo éxito, o un string con el error.
    """
    if id not in _modeloVenta.listaVentas:
        return "La venta que intentás modificar no existe."
    if productoId is not None and not ventaValidador.validarProductoId(productoId):
        return "El producto seleccionado no es válido."
    if paisId is not None and not ventaValidador.validarPaisId(paisId):
        return "El país seleccionado no es válido."
    if precioModificado is not None and not ventaValidador.validarPrecioModificado(precioModificado):
        return "El precio debe ser un número positivo."

    # Resolver nombres solo si cambiaron
    nombreProducto = None
    if productoId is not None:
        productos  = productosController.obtenerProductos()
        producto   = next((p for p in productos if p["id"] == productoId), None)
        if not producto:
            return "El producto seleccionado no existe."
        nombreProducto = producto["nombre"]

    nombrePais = None
    moneda     = None
    if paisId is not None:
        paises = paisController.obtenerPaises()
        pais   = next((p for p in paises if p["id"] == paisId), None)
        if not pais:
            return "El país seleccionado no existe."
        nombrePais = pais["nombre"]
        moneda     = pais["tipoMoneda"]

    _modeloVenta.modificarVenta(
        id               = id,
        productoId       = productoId,
        nombreProducto   = nombreProducto,
        paisId           = paisId,
        nombrePais       = nombrePais,
        moneda           = moneda,
        precioModificado = float(precioModificado) if precioModificado is not None else None,
    )
    return True


# ─────────────────────────────────────────────
#  Eliminar venta
# ─────────────────────────────────────────────
def eliminarVenta(id: int) -> bool:
    return _modeloVenta.eliminarVenta(id)


# ─────────────────────────────────────────────
#  Obtener todas las ventas
# ─────────────────────────────────────────────
def obtenerVentas() -> list[dict]:
    datos = _modeloVenta.mostrarVentas()
    return [
        {
            "id"              : id,
            "productoId"      : v["productoId"],
            "nombreProducto"  : v["nombreProducto"],
            "paisId"          : v["paisId"],
            "nombrePais"      : v["nombrePais"],
            "moneda"          : v["moneda"],
            "precioModificado": v["precioModificado"],
        }
        for id, v in datos.items()
    ]
