from model.generadorTXT import generadorTXT   # ✅ import correcto

class productos:
    
    def __init__(self):
        self.lista_productos = {}
    
    

    def agregarProducto(self, nombre, precio):
        id = len(self.lista_productos) + 1
        self.lista_productos[id] = {"nombre": nombre, "precio": precio}

        # ── Formatea el texto antes de guardar en TXT ────
        productoTxt = f"ID: {id} | Nombre: {nombre} | Precio: {precio}"

        if generadorTXT.registrarTXT(productoTxt,nombreArchivo="productos.txt"):  # ✅ llamada correcta
            return True
        return False

    def eliminarProducto(self, id):
        if id in self.lista_productos:
            
            p = self.lista_productos[id]
            itemTxt = f"ID: {id} | Nombre: {p['nombre']} | Precio: {p['precio']}"
            print(f"Eliminando del TXT: {itemTxt}")  # Debug: muestra el texto que se intentará eliminar
            resultado= generadorTXT.eliminarDelTXT(itemTxt, nombreArchivo="productos.txt")  
            print(f"Producto eliminado: {resultado  }")  # Debug: confirma eliminación
            del self.lista_productos[id]
        else:
            print("Producto no encontrado.")

    def modificarProducto(self, id, nombre=None, precio=None):
        if id in self.lista_productos:
            if nombre:
                self.lista_productos[id]["nombre"] = nombre
            if precio:
                self.lista_productos[id]["precio"] = precio
            
            p = self.lista_productos[id]
            nuevoTxt = f"ID: {id} | Nombre: {p['nombre']} | Precio: {p['precio']}"
            generadorTXT.modificarEnTXT(id, nuevoTxt, nombreArchivo="productos.txt")
        else:
            print("Producto no encontrado.")

    def mostrarProductos(self):
        return self.lista_productos