import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# ─────────────────────────────────────────────
#  Leer credenciales del .env
#  Ubicado en la raíz del proyecto
# ─────────────────────────────────────────────
_directorioActual = os.path.dirname(os.path.abspath(__file__))
_rutaEnv = os.path.normpath(os.path.join(_directorioActual, "..", ".env"))


def _cargarEnv() -> dict:
    """Lee el .env línea por línea y retorna un dict con las variables."""
    variables = {}
    if not os.path.exists(_rutaEnv):
        return variables
    with open(_rutaEnv, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, _, valor = linea.partition("=")
                variables[clave.strip()] = valor.strip()
    return variables


class gmail:

    def enviarReporte(self, destinatario: str, rutaPDF: str, nombrePais: str, moneda: str) -> bool:
        """
        Envía el PDF del reporte como adjunto al destinatario.

        Parámetros:
            destinatario : str — correo del usuario que inició sesión
            rutaPDF      : str — ruta absoluta al PDF generado
            nombrePais   : str — para el asunto y cuerpo del correo
            moneda       : str — para el cuerpo del correo

        Retorna:
            True  — si el envío fue exitoso
            False — si ocurrió algún error
        """
        try:
            env = _cargarEnv()
            remitente  = env.get("GMAIL_REMITENTE", "").strip()
            contrasena = env.get("GMAIL_APP_PASSWORD", "").strip()

            if not remitente or not contrasena:
                print("[gmail] Error: credenciales no configuradas en .env")
                return False

            if not os.path.exists(rutaPDF):
                print(f"[gmail] Error: PDF no encontrado en {rutaPDF}")
                return False

            # ── Construir el mensaje ─────────────────────────────
            mensaje = MIMEMultipart()
            mensaje["From"]    = remitente
            mensaje["To"]      = destinatario
            mensaje["Subject"] = f"Reporte de ventas — {nombrePais} ({moneda})"

            cuerpo = (
                f"Estimado usuario,\n\n"
                f"Adjunto encontrará el reporte de ventas generado para el país '{nombrePais}' "
                f"en moneda {moneda}.\n\n"
                f"El reporte presenta los productos ordenados por costo total de mayor a menor, "
                f"incluyendo el impuesto aplicado según la tarifa del país.\n\n"
                f"Saludos,\n"
                f"ATI Logística Aduanera S.A"
            )
            mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

            # ── Adjuntar el PDF ──────────────────────────────────
            nombreArchivo = os.path.basename(rutaPDF)
            print(f"[gmail] Adjuntando PDF: {nombreArchivo}")
            with open(rutaPDF, "rb") as pdf:
                adjunto = MIMEBase("application", "octet-stream")
                adjunto.set_payload(pdf.read())

                encoders.encode_base64(adjunto)
                adjunto.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=nombreArchivo
                )
                mensaje.attach(adjunto)

            # ── Enviar vía SMTP Gmail ────────────────────────────
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
                servidor.login(remitente, contrasena)
                servidor.sendmail(remitente, destinatario, mensaje.as_string())

            print(f"[gmail] Reporte enviado a: {destinatario}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("[gmail] Error de autenticación. Verifica las credenciales en .env")
            return False
        except smtplib.SMTPException as e:
            print(f"[gmail] Error SMTP: {e}")
            return False
        except Exception as e:
            print(f"[gmail] Error inesperado: {e}")
            return False
