from model import usuario as UsuarioModel
from validation import usuarioValidador
from shared import session
# ─────────────────────────────────────────────
#  Instancia única del modelo (Singleton)
# ─────────────────────────────────────────────
_modeloUsuario = UsuarioModel.usuario()


# ─────────────────────────────────────────────
#  Ingresar — registra si no existe,
#             valida coincidencia si ya existe
# ─────────────────────────────────────────────
def ingresar(username: str, correo: str) -> dict | str:
    """
    Si el usuario no existe → lo registra.
    Si existe → verifica que el correo coincida.
    En ambos casos de éxito → guarda la sesión activa en el model.
    Retorna dict del usuario o string con error.
    """
    if not usuarioValidador.validarUsername(username):
        return "El usuario no es válido. Mínimo 3 caracteres, solo letras, números, puntos y guiones bajos."
    if not usuarioValidador.validarCorreo(correo):
        return "El correo electrónico no tiene un formato válido."

    usuarioExistente = _modeloUsuario.obtenerPorUsername(username.strip())

    if not usuarioExistente:
        # ── Usuario nuevo → registrar ────────────────────
        exito = _modeloUsuario.agregarUsuario(username.strip(), correo.strip())
        if not exito:
            return "No se pudo registrar el usuario. Intenta de nuevo."
        nuevoId = max(_modeloUsuario.listaUsuarios.keys(), default=0)
        usuarioDict = {
            "id"      : nuevoId,
            "username": username.strip(),
            "correo"  : correo.strip(),
        }
    else:
        # ── Usuario existente → verificar correo ─────────
        if usuarioExistente["correo"] != correo.strip():
            return "El correo no coincide con el usuario ingresado."
        usuarioDict = usuarioExistente

    # ── Guardar sesión activa en el model ────────────────
    session.iniciar(id=usuarioDict["id"], username=usuarioDict["username"], correo=usuarioDict["correo"])
    return usuarioDict


# ─────────────────────────────────────────────
#  Sesión activa
# ─────────────────────────────────────────────
def obtenerSesion() -> dict | None:
    """Retorna el dict del usuario activo o None."""
    return session.obtener()


def cerrarSesion():
    """Limpia la sesión activa."""
    session.cerrar()


# ─────────────────────────────────────────────
#  Obtener todos los usuarios
# ─────────────────────────────────────────────
def obtenerUsuarios() -> list[dict]:
    datos = _modeloUsuario.mostrarUsuarios()
    return [
        {"id": id, "username": u["username"], "correo": u["correo"]}
        for id, u in datos.items()
    ]