import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from shared import constantes
# ─────────────────────────────────────────────
#  Ruta base → documentos/ (igual que generadorTXT)
# ─────────────────────────────────────────────
_directorioActual = os.path.dirname(os.path.abspath(__file__))
_rutaBase = os.path.normpath(os.path.join(_directorioActual, "..", "documentos"))


def _asegurarCarpeta():
    if not os.path.exists(_rutaBase):
        os.makedirs(_rutaBase)


# ─────────────────────────────────────────────
#  Colores del tema ATI
# ─────────────────────────────────────────────
COLOR_FONDO        = colors.HexColor("#121212")
COLOR_HEADER_TABLA = colors.HexColor("#1A1A2E")
COLOR_FILA_PAR     = colors.HexColor("#1E1E2E")
COLOR_FILA_IMPAR   = colors.HexColor("#252535")
COLOR_ACENTO       = colors.HexColor("#CBA6F7")
COLOR_TEXTO        = colors.HexColor("#FFFFFF")
COLOR_BORDE        = colors.HexColor("#2A2A3E")
COLOR_ROJO         = colors.HexColor("#F38BA8")


class reporte:

    def generarPDF(self, nombrePais: str, moneda: str, filas: list[dict]) -> str | None:
        """
        Genera el PDF del reporte de ventas para un país.

        Parámetros:
            nombrePais : str        — nombre del país del reporte
            moneda     : str        — moneda en que se muestran los precios
            filas      : list[dict] — lista ordenada descendente por costoTotal, cada dict:
                {
                    "nombreProducto"  : str,
                    "precioBase"      : float,
                    "impuestoPct"     : float,
                    "impuestoAplicado": float,
                    "costoTotal"      : float,
                }

        Retorna:
            str  — ruta absoluta del PDF generado
            None — si ocurrió un error
        ─────────────────────────────────────────────────────────────
        """
        try:
            _asegurarCarpeta()

            nombreArchivo = f"reporte_{nombrePais.replace(' ', '_').lower()}.pdf"
            rutaPDF       = os.path.join(_rutaBase, nombreArchivo)

            simbolos = constantes.SIMBOLOS_MONEDA
            simbolo  = simbolos.get(moneda, moneda)

            doc = SimpleDocTemplate(
                rutaPDF,
                pagesize=letter,
                leftMargin=0.75 * inch,
                rightMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch,
            )

            styles  = getSampleStyleSheet()
            story   = []

            # ── Título ───────────────────────────────────────────
            estiloTitulo = ParagraphStyle(
                "Titulo",
                parent=styles["Title"],
                textColor=COLOR_ACENTO,
                fontSize=20,
                spaceAfter=4,
            )
            estiloSubtitulo = ParagraphStyle(
                "Subtitulo",
                parent=styles["Normal"],
                textColor=colors.HexColor("#6C7086"),
                fontSize=10,
                spaceAfter=2,
            )
            estiloFormula = ParagraphStyle(
                "Formula",
                parent=styles["Normal"],
                textColor=colors.HexColor("#6C7086"),
                fontSize=9,
                spaceAfter=16,
            )

            story.append(Paragraph("ATI Logística Aduanera S.A", estiloTitulo))
            story.append(Paragraph(f"Reporte de ventas — {nombrePais}", estiloSubtitulo))
            story.append(Paragraph(f"Moneda: {moneda}  |  Ordenado por costo total descendente", estiloFormula))
            story.append(Spacer(1, 8))

            # ── Encabezado de tabla ──────────────────────────────
            encabezado = [
                Paragraph("<b>Producto</b>",          ParagraphStyle("h", textColor=COLOR_ACENTO, fontSize=9)),
                Paragraph("<b>Precio Base</b>",       ParagraphStyle("h", textColor=COLOR_ACENTO, fontSize=9)),
                Paragraph("<b>Impuesto (%)</b>",      ParagraphStyle("h", textColor=COLOR_ACENTO, fontSize=9)),
                Paragraph("<b>Impuesto Aplicado</b>", ParagraphStyle("h", textColor=COLOR_ACENTO, fontSize=9)),
                Paragraph("<b>Costo Total</b>",       ParagraphStyle("h", textColor=COLOR_ACENTO, fontSize=9)),
            ]

            datos = [encabezado]

            # ── Filas de datos ───────────────────────────────────
            for f in filas:
                estiloNormal = ParagraphStyle("n", textColor=COLOR_TEXTO, fontSize=9)
                estiloRojo   = ParagraphStyle("r", textColor=COLOR_ROJO,  fontSize=9)
                estiloCosto  = ParagraphStyle("c", textColor=COLOR_ACENTO, fontSize=9, fontName="Helvetica-Bold")

                datos.append([
                    Paragraph(f["nombreProducto"],                                      estiloNormal),
                    Paragraph(f"{simbolo} {f['precioBase']:,.2f}",                      estiloNormal),
                    Paragraph(f"{f['impuestoPct']:.1f}%",                               estiloRojo if f["impuestoPct"] > 0 else estiloNormal),
                    Paragraph(f"{simbolo} {f['impuestoAplicado']:,.2f}",                estiloRojo if f["impuestoAplicado"] > 0 else estiloNormal),
                    Paragraph(f"{simbolo} {f['costoTotal']:,.2f}",                      estiloCosto),
                ])

            # ── Estilos de tabla ─────────────────────────────────
            anchos = [2.2*inch, 1.3*inch, 1.1*inch, 1.5*inch, 1.3*inch]

            estilo = TableStyle([
                # Encabezado
                ("BACKGROUND",  (0, 0), (-1, 0),  COLOR_HEADER_TABLA),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_FILA_PAR, COLOR_FILA_IMPAR]),
                # Bordes
                ("BOX",         (0, 0), (-1, -1), 0.5, COLOR_BORDE),
                ("INNERGRID",   (0, 0), (-1, -1), 0.3, COLOR_BORDE),
                # Padding
                ("TOPPADDING",    (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                # Alineación numérica
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 0), (-1, 0),  "LEFT"),
            ])

            tabla = Table(datos, colWidths=anchos, repeatRows=1)
            tabla.setStyle(estilo)
            story.append(tabla)

            # ── Fondo oscuro en toda la página ───────────────────
            def fondoOscuro(canvas, doc):
                canvas.saveState()
                canvas.setFillColor(COLOR_FONDO)
                canvas.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)
                canvas.restoreState()

            doc.build(story, onFirstPage=fondoOscuro, onLaterPages=fondoOscuro)
            print(f"[reporte] PDF generado en: {rutaPDF}")
            return rutaPDF

        except Exception as e:
            print(f"[reporte] Error al generar PDF: {e}")
            return None