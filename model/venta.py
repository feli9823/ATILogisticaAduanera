from model.generadorTXT import generadorTXT


class venta:

    def __init__(self):
        self.listaVentas = {}

    def agregarVenta(self, productoId: int, nombreProducto: str,
                     paisId: int, nombrePais: str,
                     moneda: str, precioModificado: float) -> bool:
        id = max(self.listaVentas.keys(), default=0) + 1
        self.listaVentas[id] = {
            "productoId"      : productoId,
            "nombreProducto"  : nombreProducto,
            "paisId"          : paisId,
            "nombrePais"      : nombrePais,
            "moneda"          : moneda,
            "precioModificado": precioModificado,
        }
        ventaTxt = (
            f"ID: {id} | "
            f"Producto: {nombreProducto} (ID:{productoId}) | "
            f"Pais: {nombrePais} (ID:{paisId}) | "
            f"Moneda: {moneda} | "
            f"Precio: {precioModificado}"
        )
        if generadorTXT.registrarTXT(ventaTxt, nombreArchivo="ventas.txt"):
            return True
        return False

    def modificarVenta(self, id: int, productoId: int = None, nombreProducto: str = None,
                       paisId: int = None, nombrePais: str = None,
                       moneda: str = None, precioModificado: float = None) -> bool:
        if id not in self.listaVentas:
            return False
        v = self.listaVentas[id]
        if productoId      is not None: v["productoId"]       = productoId
        if nombreProducto  is not None: v["nombreProducto"]   = nombreProducto
        if paisId          is not None: v["paisId"]           = paisId
        if nombrePais      is not None: v["nombrePais"]       = nombrePais
        if moneda          is not None: v["moneda"]           = moneda
        if precioModificado is not None: v["precioModificado"] = precioModificado

        nuevoTxt = (
            f"ID: {id} | "
            f"Producto: {v['nombreProducto']} (ID:{v['productoId']}) | "
            f"Pais: {v['nombrePais']} (ID:{v['paisId']}) | "
            f"Moneda: {v['moneda']} | "
            f"Precio: {v['precioModificado']}"
        )
        generadorTXT.modificarEnTXT(id, nuevoTxt, nombreArchivo="ventas.txt")
        return True

    def eliminarVenta(self, id: int) -> bool:
        if id not in self.listaVentas:
            return False
        v = self.listaVentas[id]
        ventaTxt = (
            f"ID: {id} | "
            f"Producto: {v['nombreProducto']} (ID:{v['productoId']}) | "
            f"Pais: {v['nombrePais']} (ID:{v['paisId']}) | "
            f"Moneda: {v['moneda']} | "
            f"Precio: {v['precioModificado']}"
        )
        generadorTXT.eliminarDelTXT(ventaTxt, nombreArchivo="ventas.txt")
        del self.listaVentas[id]
        return True

    def mostrarVentas(self) -> dict:
        return self.listaVentas
