from model.generadorTXT import generadorTXT
from shared.constantes import ARCHIVO_PAISES

class pais:

    def __init__(self):
        self.listaPais = {}
        self._cargarDesdeTXT()

    # ─────────────────────────────────────────────
    #  Formato: ID: 1 | Nombre: Costa Rica | Impuesto: 13.0% | Moneda: CRC
    # ─────────────────────────────────────────────
    def _parsearLinea(self, linea: str) -> dict | None:
        try:
            partes = [p.strip() for p in linea.split("|")]
            return {
                "id"            : int(partes[0].split(":")[1].strip()),
                "nombre"        : partes[1].split(":", 1)[1].strip(),
                "tarifaImpuesto": float(partes[2].split(":")[1].strip().replace("%", "")),
                "tipoMoneda"    : partes[3].split(":")[1].strip(),
            }
        except Exception:
            return None

    def _cargarDesdeTXT(self):
        registros = generadorTXT.cargarDesdeTXT("paises.txt", self._parsearLinea)
        for r in registros:
            self.listaPais[r["id"]] = {
                "nombre"         : r["nombre"],
                "tarifaImpuesto" : r["tarifaImpuesto"],
                "tipoMoneda"     : r["tipoMoneda"],
            }
        print(f"[pais] {len(self.listaPais)} países cargados desde TXT.")

    def getPais(self, id):
        return self.listaPais.get(id, None)

    def agregarPais(self, nombre, tarifaImpuesto, tipoMoneda):
        id = max(self.listaPais.keys(), default=0) + 1
        self.listaPais[id] = {"nombre": nombre, "tarifaImpuesto": tarifaImpuesto, "tipoMoneda": tipoMoneda}
        paisTxt = f"ID: {id} | Nombre: {nombre} | Impuesto: {tarifaImpuesto}% | Moneda: {tipoMoneda}"
        if generadorTXT.registrarTXT(paisTxt, ARCHIVO_PAISES):
            return True
        return False

    def eliminarPais(self, id):
        if id in self.listaPais:
            p = self.listaPais[id]
            paisTxt = f"ID: {id} | Nombre: {p['nombre']} | Impuesto: {p['tarifaImpuesto']}% | Moneda: {p['tipoMoneda']}"
            generadorTXT.eliminarDelTXT(paisTxt, ARCHIVO_PAISES)
            del self.listaPais[id]
        else:
            print("Pais no encontrado.")

    def modificarPais(self, id, nombre=None, tarifaImpuesto=None, tipoMoneda=None):
        if id in self.listaPais:
            if nombre         is not None: self.listaPais[id]["nombre"]         = nombre
            if tarifaImpuesto is not None: self.listaPais[id]["tarifaImpuesto"] = tarifaImpuesto
            if tipoMoneda     is not None: self.listaPais[id]["tipoMoneda"]     = tipoMoneda
            p = self.listaPais[id]
            nuevoTxt = f"ID: {id} | Nombre: {p['nombre']} | Impuesto: {p['tarifaImpuesto']}% | Moneda: {p['tipoMoneda']}"
            generadorTXT.modificarEnTXT(id, nuevoTxt, ARCHIVO_PAISES)
        else:
            print("Pais no encontrado.")

    def mostrarPais(self):
        return self.listaPais

    