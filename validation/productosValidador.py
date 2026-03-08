import re

def validarNombre(nombre: str) -> bool:
    if not isinstance(nombre, str) or not nombre.strip():
        return False
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$", nombre.strip()):
        return False
    return True



def validarPrecio(precio):
    try:
        if precio != float(precio):
            raise ValueError("El precio debe ser un número.")
        precio = float(precio)
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
    except ValueError as e:
        print(f"Error: {e}")
        return False
    return True


