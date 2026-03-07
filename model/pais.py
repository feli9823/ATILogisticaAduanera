class pais:

    def __init__(self):
       self.listaPais = {}
    
    
    def agregarPais(self, nombre, tarifaImpuesto, tipoMoneda):
        id=len(self.listaPais)+1
        self.listaPais[id] = {"nombre": nombre, "tarifaImpuesto": tarifaImpuesto, "tipoMoneda": tipoMoneda}

    def eliminarPais(self, id):
        if id in self.listaPais:
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
        else:
            print("Pais no encontrado.")
    
    def mostrarPais(self):
        return self.listaPais