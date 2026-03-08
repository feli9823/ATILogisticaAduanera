from model import reporte as ReporteModel
from controller import ventaController, paisController, conversorController
from shared import constantes
# ─────────────────────────────────────────────
#  Instancia única del modelo (Singleton)
# ─────────────────────────────────────────────
_modeloReporte = ReporteModel.reporte()


# ─────────────────────────────────────────────
#  Generar reporte PDF (RF-17, RF-18, RF-19)
# ─────────────────────────────────────────────
def generarReporte(nombrePais: str, moneda: str) -> str:
    """
    Orquesta la generación del reporte:
      1. Obtiene ventas del país seleccionado
      2. Obtiene el impuesto del país
      3. Calcula costo total con conversorController si la moneda difiere
      4. Ordena descendente por costo total
      5. Delega al model para generar el PDF

    Retorna:
        str — ruta del PDF si tuvo éxito
        str — mensaje de error si falló
    """
    if not nombrePais or not nombrePais.strip():
        return "Debes seleccionar un país."
    if not moneda or moneda not in constantes.MONEDAS_VALIDAS:
        return "Debes seleccionar una moneda válida."

    # ── 1. Obtener el país para sacar su impuesto ────────
    paises = paisController.obtenerPaises()
    pais   = next((p for p in paises if p["nombre"] == nombrePais), None)
    if not pais:
        return f"El país '{nombrePais}' no existe en el sistema."

    impuestoPct = pais["tarifaImpuesto"]

    # ── 2. Filtrar ventas del país ───────────────────────
    todasVentas  = ventaController.obtenerVentas()
    ventasPais   = [v for v in todasVentas if v["paisId"] == pais["id"]]

    if not ventasPais:
        return f"No hay ventas registradas para '{nombrePais}'."

    # ── 3. Calcular costos y convertir moneda ────────────
    filas = []
    for v in ventasPais:
        precioBase = v["precioModificado"]
        costoTotal = precioBase + (precioBase * (impuestoPct / 100))
        impuestoAplicado = costoTotal - precioBase

        # Convertir si la moneda del reporte difiere a la de la venta
        if moneda != v["moneda"]:
            precioBase       = conversorController.convertir(precioBase,       v["moneda"], moneda)
            impuestoAplicado = conversorController.convertir(impuestoAplicado, v["moneda"], moneda)
            costoTotal       = conversorController.convertir(costoTotal,       v["moneda"], moneda)

            if isinstance(precioBase,       str): precioBase       = 0.0
            if isinstance(impuestoAplicado, str): impuestoAplicado = 0.0
            if isinstance(costoTotal,       str): costoTotal       = 0.0

        filas.append({
            "nombreProducto"  : v["nombreProducto"],
            "precioBase"      : float(precioBase),
            "impuestoPct"     : impuestoPct,
            "impuestoAplicado": float(impuestoAplicado),
            "costoTotal"      : float(costoTotal),
        })

    # ── 4. Ordenar descendente por costo total (RF-17) ───
    filas.sort(key=lambda f: f["costoTotal"], reverse=True)

    # ── 5. Generar PDF (RF-19) ───────────────────────────
    rutaPDF = _modeloReporte.generarPDF(
        nombrePais = nombrePais,
        moneda     = moneda,
        filas      = filas,
    )

    if not rutaPDF:
        return "Error al generar el PDF. Revisa los logs."

    return rutaPDF


# ─────────────────────────────────────────────
#  Obtener nombres de países disponibles
#  (para poblar el dropdown del diálogo)
# ─────────────────────────────────────────────
def obtenerNombresPaises() -> list[str]:
    return [p["nombre"] for p in paisController.obtenerPaises()]