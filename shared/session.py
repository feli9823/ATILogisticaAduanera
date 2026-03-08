_sesion_activa: dict | None = None

def iniciar(id: int, username: str, correo: str) -> None:
    global _sesion_activa
    _sesion_activa = {"id": id, "username": username, "correo": correo}

def obtener() -> dict | None:
    return _sesion_activa

def cerrar() -> None:
    global _sesion_activa
    _sesion_activa = None