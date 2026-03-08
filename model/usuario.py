from model.generadorTXT import generadorTXT


class usuario:

    def __init__(self):
        self.listaUsuarios = {}

    def agregarUsuario(self, username: str, correo: str) -> bool:
        id = max(self.listaUsuarios.keys(), default=0) + 1
        self.listaUsuarios[id] = {
            "username": username,
            "correo"  : correo,
        }
        usuarioTxt = f"ID: {id} | Usuario: {username} | Correo: {correo}"
        if generadorTXT.registrarTXT(usuarioTxt, nombreArchivo="usuarios.txt"):
            return True
        return False

    def obtenerPorUsername(self, username: str) -> dict | None:
        for id, u in self.listaUsuarios.items():
            if u["username"] == username:
                return {"id": id, **u}
        return None

    def obtenerPorCorreo(self, correo: str) -> dict | None:
        for id, u in self.listaUsuarios.items():
            if u["correo"] == correo:
                return {"id": id, **u}
        return None

    def mostrarUsuarios(self) -> dict:
        return self.listaUsuarios
