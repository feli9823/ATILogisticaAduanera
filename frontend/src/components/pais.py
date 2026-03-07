import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal


# ─────────────────────────────────────────────
#  Monedas disponibles (RF-13)
# ─────────────────────────────────────────────
monedasDisponibles = [
    ft.dropdown.Option(key="CRC", text="₡ Colones (CRC)"),
    ft.dropdown.Option(key="USD", text="$ Dólares (USD)"),
    ft.dropdown.Option(key="EUR", text="€ Euros (EUR)"),
    ft.dropdown.Option(key="BRL", text="R$ Reales Brasileños (BRL)"),
]

# ─────────────────────────────────────────────
#  Datos en memoria
# ─────────────────────────────────────────────
listaPaises: list[dict] = []
nextId = 1


# ─────────────────────────────────────────────
#  Utilidades para diálogos
# ─────────────────────────────────────────────
def abrirDialogo(page: ft.Page, dlg: ft.AlertDialog):
    if dlg not in page.overlay:
        page.overlay.append(dlg)
    dlg.open = True
    page.update()


def cerrarDialogo(page: ft.Page, dlg: ft.AlertDialog):
    dlg.open = False
    page.update()


# ─────────────────────────────────────────────
#  Diálogo: Añadir / Editar país
# ─────────────────────────────────────────────
def dialogoPais(page: ft.Page, onGuardar, pais: dict = None) -> ft.AlertDialog:
    esEdicion = pais is not None

    campoNombre = ft.TextField(
        label="Nombre del país",
        value=pais["nombre"] if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )

    # RF-12: tarifa de impuesto
    campoImpuesto = ft.TextField(
        label="Tarifa de impuesto (%)",
        value=str(pais["impuesto"]) if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=320,
    )

    # RF-13: selección de moneda
    campoMoneda = ft.Dropdown(
        label="Moneda",
        value=pais["moneda"] if esEdicion else "USD",
        options=monedasDisponibles,
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )

    errorTxt = ft.Text("", color=ft.Colors.RED_400, size=12)

    def guardar(e):
        if not campoNombre.value.strip():
            errorTxt.value = "El nombre del país es obligatorio."
            errorTxt.update()
            return
        if not campoImpuesto.value.strip():
            errorTxt.value = "La tarifa de impuesto es obligatoria."
            errorTxt.update()
            return
        try:
            impuesto = float(campoImpuesto.value.strip())
            if impuesto < 0 or impuesto > 100:
                raise ValueError
        except ValueError:
            errorTxt.value = "La tarifa debe ser un número entre 0 y 100."
            errorTxt.update()
            return

        onGuardar({
            "nombre"  : campoNombre.value.strip(),
            "impuesto": impuesto,
            "moneda"  : campoMoneda.value or "USD",
        })
        cerrarDialogo(page, dlg)

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Editar país" if esEdicion else "Añadir país",
            color=constants.TEXT_COLOR,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Column(
            tight=True,
            spacing=12,
            controls=[campoNombre, campoImpuesto, campoMoneda, errorTxt],
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: cerrarDialogo(page, dlg),
                style=ft.ButtonStyle(color="#6C7086"),
            ),
            ft.Button(
                "Guardar",
                on_click=guardar,
                style=ft.ButtonStyle(
                    bgcolor=constants.btnAddBg,
                    color=constants.btnAddText,
                ),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dlg


# ─────────────────────────────────────────────
#  Diálogo: Ver país
# ─────────────────────────────────────────────
def dialogoVer(page: ft.Page, pais: dict) -> ft.AlertDialog:

    def filaDetalle(label, valor):
        return ft.Row(
            controls=[
                ft.Text(label, color="#6C7086", size=13, width=160),
                ft.Text(str(valor), color=constants.TEXT_COLOR, size=13),
            ],
        )

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Detalle del país",
            color=constants.TEXT_COLOR,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Column(
            tight=True,
            spacing=10,
            controls=[
                filaDetalle("ID",               pais["id"]),
                filaDetalle("Nombre",           pais["nombre"]),
                filaDetalle("Tarifa impuesto",  f"{pais['impuesto']}%"),
                filaDetalle("Moneda",           pais["moneda"]),
            ],
        ),
        actions=[
            ft.TextButton(
                "Cerrar",
                on_click=lambda e: cerrarDialogo(page, dlg),
                style=ft.ButtonStyle(color=constants.accentColor),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dlg


# ─────────────────────────────────────────────
#  Diálogo: Eliminar país
# ─────────────────────────────────────────────
def dialogoEliminar(page: ft.Page, pais: dict, onConfirmar) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Eliminar país",
            color=ft.Colors.RED_400,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Text(
            f'¿Estás seguro de eliminar "{pais["nombre"]}"?',
            color=constants.TEXT_COLOR,
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: cerrarDialogo(page, dlg),
                style=ft.ButtonStyle(color="#6C7086"),
            ),
            ft.Button(
                "Eliminar",
                on_click=lambda e: [onConfirmar(), cerrarDialogo(page, dlg)],
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_700,
                    color=constants.TEXT_COLOR,
                ),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dlg


# ─────────────────────────────────────────────
#  Vista principal de País
# ─────────────────────────────────────────────
def pais(router) -> ft.Control:
    global nextId

    tablaRef = ft.Ref[ft.DataTable]()

    def construirFilas() -> list[ft.DataRow]:
        if not listaPaises:
            return []

        filas = []
        for i, p in enumerate(listaPaises):
            bgColor = constants.tableRowBg if i % 2 == 0 else constants.tableRowAlt

            def onVer(e, item=p):
                dlg = dialogoVer(router.page, item)
                abrirDialogo(router.page, dlg)

            def onEditar(e, item=p):
                def guardarEdicion(datos):
                    item["nombre"]   = datos["nombre"]
                    item["impuesto"] = datos["impuesto"]
                    item["moneda"]   = datos["moneda"]
                    refrescar()
                dlg = dialogoPais(router.page, guardarEdicion, item)
                abrirDialogo(router.page, dlg)

            def onEliminar(e, item=p):
                def confirmar():
                    listaPaises.remove(item)
                    refrescar()
                dlg = dialogoEliminar(router.page, item, confirmar)
                abrirDialogo(router.page, dlg)

            filas.append(
                ft.DataRow(
                    color=bgColor,
                    cells=[
                        ft.DataCell(ft.Text(str(p["id"]),         color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(p["nombre"],          color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(f"{p['impuesto']}%",  color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.VISIBILITY_OUTLINED,
                                        icon_color="#6C7086",
                                        tooltip="Ver",
                                        on_click=onVer,
                                        icon_size=18,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        icon_color=constants.accentColor,
                                        tooltip="Editar",
                                        on_click=onEditar,
                                        icon_size=18,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.RED_400,
                                        tooltip="Eliminar",
                                        on_click=onEliminar,
                                        icon_size=18,
                                    ),
                                ],
                            )
                        ),
                    ],
                )
            )
        return filas

    def refrescar():
        tablaRef.current.rows = construirFilas()
        tablaRef.current.update()

    def abrirDialogoAgregar(e):
        global nextId

        def guardarNuevo(datos):
            global nextId
            listaPaises.append({
                "id"      : nextId,
                "nombre"  : datos["nombre"],
                "impuesto": datos["impuesto"],
                "moneda"  : datos["moneda"],
            })
            nextId += 1
            refrescar()

        dlg = dialogoPais(router.page, guardarNuevo)
        abrirDialogo(router.page, dlg)

    tabla = ft.DataTable(
        ref=tablaRef,
        border=ft.Border.all(1, constants.borderColor),
        border_radius=8,
        horizontal_lines=ft.BorderSide(1, constants.borderColor),
        heading_row_color=constants.tableHeaderBg,
        heading_row_height=48,
        data_row_min_height=48,
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("ID",                color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Nombre País",       color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Tarifa Impuesto",   color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Acciones",          color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
        ],
        rows=construirFilas(),
    )

    contenido = ft.Container(
        expand=True,
        bgcolor=constants.BG_COLOR,
        padding=ft.Padding.all(32),
        content=ft.Column(
            expand=True,
            spacing=24,
            controls=[
                ft.Text(
                    "Lista de países",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=constants.TEXT_COLOR,
                ),
                ft.Divider(color=constants.borderColor),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[tabla],
                    ),
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD, color=constants.btnAddText, size=18),
                                    ft.Text("Añadir país", color=constants.btnAddText, weight=ft.FontWeight.W_600),
                                ],
                                spacing=8,
                                tight=True,
                            ),
                            on_click=abrirDialogoAgregar,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.DEFAULT: constants.btnAddBg,
                                    ft.ControlState.HOVERED: "#A78BDA",
                                },
                                color=constants.btnAddText,
                                padding=ft.Padding.symmetric(vertical=12, horizontal=24),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    return layoutPrincipal(router, contenido, activePage="pais")