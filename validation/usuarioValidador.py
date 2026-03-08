import re

def validarUsername(username: str) -> bool:
    if not isinstance(username, str) or not username.strip():
        return False
    # Solo letras, números, puntos y guiones bajos, mínimo 3 caracteres
    if not re.match(r"^[a-zA-Z0-9._]{3,}$", username.strip()):
        return False
    return True

def validarCorreo(correo: str) -> bool:
    if not isinstance(correo, str) or not correo.strip():
        return False
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", correo.strip()):
        return False
    return True
