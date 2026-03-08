from model import gmail as GmailModel
from controller import reporteController

# ─────────────────────────────────────────────
#  Instancia única del modelo (Singleton)
# ─────────────────────────────────────────────
_modeloGmail = GmailModel.gmail()


# ─────────────────────────────────────────────
#  Enviar reporte por correo (RF-20)
# ─────────────────────────────────────────────
def enviarReporte(correoDestino: str, nombrePais: str, moneda: str) -> bool | str:
    """
    Genera el PDF y lo envía al correo del usuario.

    Parámetros:
        correoDestino : str — correo del usuario en sesión
        nombrePais    : str — país del reporte
        moneda        : str — moneda seleccionada

    Retorna:
        True — si generó y envió correctamente
        str  — mensaje de error si algo falló
    """
    if not correoDestino or "@" not in correoDestino:
        return "El correo del destinatario no es válido."

    # ── 1. Generar el PDF ────────────────────────────────
    resultado = reporteController.generarReporte(nombrePais, moneda)

    # generarReporte retorna la ruta si éxito, o un str de error
    if isinstance(resultado, str) and not resultado.endswith(".pdf"):
        return resultado or "No se pudo generar el PDF."

    rutaPDF = resultado

    # ── 2. Enviar el PDF ─────────────────────────────────
    exito = _modeloGmail.enviarReporte(
        destinatario = correoDestino,
        rutaPDF      = rutaPDF,
        nombrePais   = nombrePais,
        moneda       = moneda,
    )

    if not exito:
        return "No se pudo enviar el correo. Verifica las credenciales en el archivo .env"

    return True
