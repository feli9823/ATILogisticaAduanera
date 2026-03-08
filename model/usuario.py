from model.generadorTXT import generadorTXT
from shared.constantes import ARCHIVO_USUARIOS
class usuario:

    def __init__(self):
        self.listaUsuarios  = {}
        self._cargarDesdeTXT()

    # ─────────────────────────────────────────────
    #  Formato: ID: 1 | Usuario: juan | Correo: juan@mail.com
    # ─────────────────────────────────────────────
    def _parsearLinea(self, linea: str) -> dict | None:
        try:
            partes = [p.strip() for p in linea.split("|")]
            return {
                "id"      : int(partes[0].split(":")[1].strip()),
                "username": partes[1].split(":", 1)[1].strip(),
                "correo"  : partes[2].split(":", 1)[1].strip(),
            }
        except Exception:
            return None

    def _cargarDesdeTXT(self):
        registros = generadorTXT.cargarDesdeTXT("usuarios.txt", self._parsearLinea)
        for r in registros:
            self.listaUsuarios[r["id"]] = {"username": r["username"], "correo": r["correo"]}
        print(f"[usuario] {len(self.listaUsuarios)} usuarios cargados desde TXT.")

    
    # ── CRUD ─────────────────────────────────────
    def agregarUsuario(self, username: str, correo: str) -> bool:
        id = max(self.listaUsuarios.keys(), default=0) + 1
        self.listaUsuarios[id] = {"username": username, "correo": correo}
        usuarioTxt = f"ID: {id} | Usuario: {username} | Correo: {correo}"
        return generadorTXT.registrarTXT(usuarioTxt, ARCHIVO_USUARIOS)

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