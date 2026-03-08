from validation.nameValidator import validarNombre


def validarPrecio(precio):
    try:
        precio = float(precio)
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
    except ValueError as e:
        print(f"Error: {e}")
        return False
    return True


