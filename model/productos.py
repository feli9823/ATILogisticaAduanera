from model.generadorTXT import generadorTXT
from shared.constantes import ARCHIVO_PRODUCTOS
class productos:

    def __init__(self):
        self.listaProductos = {}
        self._cargarDesdeTXT()

    # ─────────────────────────────────────────────
    #  Formato: ID: 1 | Nombre: Laptop | Precio: 500000.0
    # ─────────────────────────────────────────────
    def _parsearLinea(self, linea: str) -> dict | None:
        try:
            partes = [p.strip() for p in linea.split("|")]
            return {
                "id"    : int(partes[0].split(":")[1].strip()),
                "nombre": partes[1].split(":", 1)[1].strip(),
                "precio": float(partes[2].split(":")[1].strip()),
            }
        except Exception:
            return None

    def _cargarDesdeTXT(self):
        registros = generadorTXT.cargarDesdeTXT("productos.txt", self._parsearLinea)
        for r in registros:
            self.listaProductos[r["id"]] = {"nombre": r["nombre"], "precio": r["precio"]}
        print(f"[productos] {len(self.listaProductos)} productos cargados desde TXT.")

    def agregarProducto(self, nombre, precio):
        id = max(self.listaProductos.keys(), default=0) + 1
        self.listaProductos[id] = {"nombre": nombre, "precio": precio}
        productoTxt = f"ID: {id} | Nombre: {nombre} | Precio: {precio}"
        if generadorTXT.registrarTXT(productoTxt, ARCHIVO_PRODUCTOS):
            return True
        return False

    def eliminarProducto(self, id):
        if id in self.listaProductos:
            p = self.listaProductos[id]
            itemTxt = f"ID: {id} | Nombre: {p['nombre']} | Precio: {p['precio']}"
            print(f"Eliminando del TXT: {itemTxt}")
            resultado = generadorTXT.eliminarDelTXT(itemTxt, ARCHIVO_PRODUCTOS)
            print(f"Producto eliminado: {resultado}")
            del self.listaProductos[id]
        else:
            print("Producto no encontrado.")

    def modificarProducto(self, id, nombre=None, precio=None):
        if id in self.listaProductos:
            if nombre is not None: self.listaProductos[id]["nombre"] = nombre
            if precio  is not None: self.listaProductos[id]["precio"] = precio
            p = self.listaProductos[id]
            nuevoTxt = f"ID: {id} | Nombre: {p['nombre']} | Precio: {p['precio']}"
            generadorTXT.modificarEnTXT(id, nuevoTxt, ARCHIVO_PRODUCTOS)
        else:
            print("Producto no encontrado.")

    def mostrarProductos(self):
        return self.listaProductos