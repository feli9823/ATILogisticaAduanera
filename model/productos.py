class productos:
    
    def __init__(self):
        self.lista_productos = {}
    

    def agregarProducto(self, nombre, precio):
        id=len(self.lista_productos)+1
        self.lista_productos[id] = {"nombre": nombre, "precio": precio}
    

    def eliminarProducto(self, id):
        if id in self.lista_productos:
            del self.lista_productos[id]
        else:
            print("Producto no encontrado.")
    

    def modificarProducto(self, id, nombre=None, precio=None):
        if id in self.lista_productos:
            if nombre:
                self.lista_productos[id]["nombre"] = nombre
            if precio:
                self.lista_productos[id]["precio"] = precio
        else:
            print("Producto no encontrado.")
    

    def mostrarProductos(self):
       return self.lista_productos