from model.generadorTXT import generadorTXT

class pais:

    def __init__(self):
        self.listaPais = {}

    def getPais(self, id):
        return self.listaPais.get(id, None)

    def agregarPais(self, nombre, tarifaImpuesto, tipoMoneda):
        id = len(self.listaPais) + 1
        self.listaPais[id] = {
            "nombre"         : nombre,
            "tarifaImpuesto" : tarifaImpuesto,
            "tipoMoneda"     : tipoMoneda,
        }
        paisTxt = f"ID: {id} | Nombre: {nombre} | Impuesto: {tarifaImpuesto}% | Moneda: {tipoMoneda}"
        if generadorTXT.registrarTXT(paisTxt, nombreArchivo="paises.txt"):
            return True
        return False

    def eliminarPais(self, id):
        if id in self.listaPais:
            p = self.listaPais[id]
            paisTxt = f"ID: {id} | Nombre: {p['nombre']} | Impuesto: {p['tarifaImpuesto']}% | Moneda: {p['tipoMoneda']}"
            generadorTXT.eliminarDelTXT(paisTxt, nombreArchivo="paises.txt")
            del self.listaPais[id]
        else:
            print("Pais no encontrado.")

    def modificarPais(self, id, nombre=None, tarifaImpuesto=None, tipoMoneda=None):
        if id in self.listaPais:
            if nombre:
                self.listaPais[id]["nombre"] = nombre
            if tarifaImpuesto:
                self.listaPais[id]["tarifaImpuesto"] = tarifaImpuesto
            if tipoMoneda:
                self.listaPais[id]["tipoMoneda"] = tipoMoneda

            p = self.listaPais[id]
            nuevoTxt = f"ID: {id} | Nombre: {p['nombre']} | Impuesto: {p['tarifaImpuesto']}% | Moneda: {p['tipoMoneda']}"
            generadorTXT.modificarEnTXT(id, nuevoTxt, nombreArchivo="paises.txt")
        else:
            print("Pais no encontrado.")

    def mostrarPais(self):
        return self.listaPais