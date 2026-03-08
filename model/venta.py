from model.generadorTXT import generadorTXT
from shared.constantes import ARCHIVO_VENTAS

class venta:

    def __init__(self):
        self.listaVentas = {}
        self._cargarDesdeTXT()

    # ─────────────────────────────────────────────
    #  Formato: ID: 1 | Producto: Laptop (ID:1) | Pais: Costa Rica (ID:2) | Moneda: CRC | Precio: 500000.0
    # ─────────────────────────────────────────────
    def _parsearLinea(self, linea: str) -> dict | None:
        try:
            partes = [p.strip() for p in linea.split("|")]
            id = int(partes[0].split(":")[1].strip())

            prodRaw        = partes[1].split(":", 1)[1].strip()
            nombreProducto = prodRaw[:prodRaw.rfind("(")].strip()
            productoId     = int(prodRaw[prodRaw.rfind("ID:") + 3 : prodRaw.rfind(")")])

            paisRaw    = partes[2].split(":", 1)[1].strip()
            nombrePais = paisRaw[:paisRaw.rfind("(")].strip()
            paisId     = int(paisRaw[paisRaw.rfind("ID:") + 3 : paisRaw.rfind(")")])

            return {
                "id"              : id,
                "productoId"      : productoId,
                "nombreProducto"  : nombreProducto,
                "paisId"          : paisId,
                "nombrePais"      : nombrePais,
                "moneda"          : partes[3].split(":")[1].strip(),
                "precioModificado": float(partes[4].split(":")[1].strip()),
            }
        except Exception:
            return None

    def _cargarDesdeTXT(self):
        registros = generadorTXT.cargarDesdeTXT("ventas.txt", self._parsearLinea)
        for r in registros:
            self.listaVentas[r["id"]] = {k: v for k, v in r.items() if k != "id"}
        print(f"[venta] {len(self.listaVentas)} ventas cargadas desde TXT.")

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
        if generadorTXT.registrarTXT(ventaTxt, ARCHIVO_VENTAS):
            return True
        return False

    def modificarVenta(self, id: int, productoId: int = None, nombreProducto: str = None,
                       paisId: int = None, nombrePais: str = None,
                       moneda: str = None, precioModificado: float = None) -> bool:
        if id not in self.listaVentas:
            return False
        v = self.listaVentas[id]
        if productoId       is not None: v["productoId"]       = productoId
        if nombreProducto   is not None: v["nombreProducto"]   = nombreProducto
        if paisId           is not None: v["paisId"]           = paisId
        if nombrePais       is not None: v["nombrePais"]       = nombrePais
        if moneda           is not None: v["moneda"]           = moneda
        if precioModificado is not None: v["precioModificado"] = precioModificado
        nuevoTxt = (
            f"ID: {id} | "
            f"Producto: {v['nombreProducto']} (ID:{v['productoId']}) | "
            f"Pais: {v['nombrePais']} (ID:{v['paisId']}) | "
            f"Moneda: {v['moneda']} | "
            f"Precio: {v['precioModificado']}"
        )
        generadorTXT.modificarEnTXT(id, nuevoTxt, ARCHIVO_VENTAS)
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
        generadorTXT.eliminarDelTXT(ventaTxt, ARCHIVO_VENTAS)
        del self.listaVentas[id]
        return True

    def mostrarVentas(self) -> dict:
        return self.listaVentas