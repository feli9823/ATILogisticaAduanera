import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal
from components.ventas import listaVentas
from components.pais import listaPaises


TODAS_MONEDAS = "TODAS"

monedasFiltro = [
    ft.dropdown.Option(key=TODAS_MONEDAS, text="Todas las monedas"),
    ft.dropdown.Option(key="CRC", text="₡ Colones (CRC)"),
    ft.dropdown.Option(key="USD", text="$ Dólares (USD)"),
    ft.dropdown.Option(key="EUR", text="€ Euros (EUR)"),
    ft.dropdown.Option(key="BRL", text="R$ Reales Brasileños (BRL)"),
]

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def obtenerImpuestoPais(paisId: int) -> float:
    """ Obtiene la tarifa de impuesto del país registrado."""
    pais = next((p for p in listaPaises if p["id"] == paisId), None)
    return pais["impuesto"] if pais else 0.0


def calcularCostoTotal(precio: float, impuestoPct: float) -> float:
    """ CostoTotal = Precio + (Precio * Impuesto)"""
    return precio + (precio * (impuestoPct / 100))


def formatearMoneda(valor: float, moneda: str) -> str:
    simbolos = {"CRC": "₡", "USD": "$", "EUR": "€", "BRL": "R$"}
    simbolo = simbolos.get(moneda, moneda)
    return f"{simbolo} {valor:,.2f}"


# ─────────────────────────────────────────────
#  Vista principal de Consultas de Ventas
# ─────────────────────────────────────────────
def consultasVentas(router) -> ft.Control:

    tablaRef   = ft.Ref[ft.DataTable]()
    sinDataRef = ft.Ref[ft.Container]()
    filtroRef  = ft.Ref[ft.Dropdown]()

    def construirFilas(monedaDestino: str = TODAS_MONEDAS) -> list[ft.DataRow]:
        if not listaVentas:
            return []

        filas = []
        for i, v in enumerate(listaVentas):
            bgColor     = constants.tableRowBg if i % 2 == 0 else constants.tableRowAlt
            impuestoPct = obtenerImpuestoPais(v["paisId"])   # RF-14
            precioBase  = v["precioModificado"]
            costoTotal  = calcularCostoTotal(precioBase, impuestoPct)  # RF-15
            impuestoVal = costoTotal - precioBase




            if monedaDestino != TODAS_MONEDAS and monedaDestino != v["moneda"]:
                print(
                    f"[CONVERSION PENDIENTE] "
                    f"producto='{v['nombreProducto']}' | "
                    f"moneda_origen='{v['moneda']}' | "
                    f"moneda_destino='{monedaDestino}' | "
                    f"precioBase={precioBase} | "
                    f"impuestoVal={impuestoVal:.4f} | "
                    f"costoTotal={costoTotal:.4f}"
                )
            # ─────────────────────────────────────────────────────────────

            monedaMostrar = monedaDestino if monedaDestino != TODAS_MONEDAS else v["moneda"]

            filas.append(
                ft.DataRow(
                    color=bgColor,
                    cells=[
                        ft.DataCell(ft.Text(v["nombreProducto"],               color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(v["nombrePais"],                   color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(formatearMoneda(precioBase, monedaMostrar),  color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(f"{impuestoPct:.1f}%",
                            color="#F38BA8" if impuestoPct > 0 else "#6C7086", size=13)),
                        ft.DataCell(ft.Text(formatearMoneda(impuestoVal, monedaMostrar),
                            color="#F38BA8" if impuestoVal > 0 else "#6C7086", size=13)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    formatearMoneda(costoTotal, monedaMostrar),
                                    color=constants.accentColor,
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                ),
                                bgcolor="#2A1F3D",
                                border_radius=6,
                                padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                            )
                        ),
                    ],
                )
            )
        return filas

    def refrescar(monedaFiltro: str = TODAS_MONEDAS):
        filas = construirFilas(monedaFiltro)
        tablaRef.current.rows   = filas
        tablaRef.current.visible   = len(filas) > 0
        sinDataRef.current.visible = len(filas) == 0
        tablaRef.current.update()
        sinDataRef.current.update()

    def onCambioMoneda(e):
        refrescar(filtroRef.current.value or TODAS_MONEDAS)

    tabla = ft.DataTable(
        ref=tablaRef,
        border=ft.Border.all(1, constants.borderColor),
        border_radius=8,
        horizontal_lines=ft.BorderSide(1, constants.borderColor),
        heading_row_color=constants.tableHeaderBg,
        heading_row_height=48,
        data_row_min_height=48,
        expand=True,
        visible=len(listaVentas) > 0,
        columns=[
            ft.DataColumn(ft.Text("Producto",          color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("País",              color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Precio Base",       color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Impuesto (%)",      color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Impuesto Aplicado", color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Costo Total",       color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
        ],
        rows=construirFilas(),
    )

    sinDatos = ft.Container(
        ref=sinDataRef,
        visible=len(listaVentas) == 0,
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            tight=True,
            controls=[
                ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, color="#6C7086", size=48),
                ft.Text("No hay ventas registradas para consultar.", color="#6C7086", size=14),
                ft.Text("Registra ventas en el módulo 'Ventas' primero.", color="#3C3C4E", size=12),
            ],
        ),
    )

    filtroMoneda = ft.Dropdown(
        ref=filtroRef,
        label="Visualizar en moneda",
        value=TODAS_MONEDAS,
        options=monedasFiltro,
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=240,
        on_select=onCambioMoneda,
    )

    contenido = ft.Container(
        expand=True,
        bgcolor=constants.BG_COLOR,
        padding=ft.Padding.all(32),
        content=ft.Column(
            expand=True,
            spacing=24,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(
                            "Consulta de precios e impuestos",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=constants.TEXT_COLOR,
                        ),
                    ],
                ),
                ft.Divider(color=constants.borderColor),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FILTER_LIST_ROUNDED, color=constants.accentColor, size=20),
                        ft.Text("Filtrar por moneda:", color="#6C7086", size=13),
                        filtroMoneda,
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(
                    expand=True,
                    content=ft.Stack(
                        expand=True,
                        controls=[
                            ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[tabla],
                            ),
                            sinDatos,
                        ],
                    ),
                ),
            ],
        ),
    )

    return layoutPrincipal(router, contenido, activePage="consultas_ventas")