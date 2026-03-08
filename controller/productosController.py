from model import productos as ProductosModel
from validation import productosValidador

_modeloProductos = ProductosModel.productos()


# ─────────────────────────────────────────────
#  Guardar producto
# ─────────────────────────────────────────────
def guardarProducto(nombre: str, precio: float) -> dict | str:
    """
    Valida y guarda un nuevo producto.
    Retorna el producto creado como dict si tuvo éxito,
    o un string con el mensaje de error si falló.
    """
    if not productosValidador.validarNombre(nombre):
        return "El nombre del producto no es válido. Solo se permiten letras, espacios y guiones."
    if not productosValidador.validarPrecio(precio):
        return "El precio debe ser un número positivo."

    exito = _modeloProductos.agregarProducto(nombre, precio)
    if not exito:
        return "No se pudo guardar el producto. Intenta de nuevo."

    nuevoId = max(_modeloProductos.listaProductos.keys(), default=0)
    return {
        "id"    : nuevoId,
        "nombre": nombre,
        "precio": precio,
    }


# ─────────────────────────────────────────────
#  Modificar producto
# ─────────────────────────────────────────────
def modificarProducto(id: int, nombre: str = None, precio: float = None) -> bool | str:
    """
    Modifica un producto existente por id.
    Retorna True si se modificó,
    o un string con el mensaje de error si falló.
    """
    if id not in _modeloProductos.listaProductos:
        return "El producto que intentás modificar no existe."
    if nombre is not None and not productosValidador.validarNombre(nombre):
        return "El nombre del producto no es válido. Solo se permiten letras, espacios y guiones."
    if precio is not None and not productosValidador.validarPrecio(precio):
        return "El precio debe ser un número positivo."

    _modeloProductos.modificarProducto(id, nombre=nombre, precio=precio)
    return True


# ─────────────────────────────────────────────
#  Eliminar producto
# ─────────────────────────────────────────────
def eliminarProducto(id: int) -> bool:
    """
    Elimina un producto por id.
    Retorna True si se eliminó, False si no existía.
    """
    if id not in _modeloProductos.listaProductos:
        return False
    _modeloProductos.eliminarProducto(id)
    return True


# ─────────────────────────────────────────────
#  Obtener todos los productos
# ─────────────────────────────────────────────
def obtenerProductos() -> list[dict]:
    """
    Retorna todos los productos para mostrar en la tabla.
    Formato: [{"id": 1, "nombre": "...", "precio": 0.0}, ...]
    """
    datos = _modeloProductos.mostrarProductos()
    return [
        {
            "id"    : id,
            "nombre": p["nombre"],
            "precio": p["precio"],
        }
        for id, p in datos.items()
    ]