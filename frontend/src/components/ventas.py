import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal
from controller import ventaController, productosController, paisController


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
#  Diálogo: Añadir / Editar venta
# ─────────────────────────────────────────────
def dialogoVenta(page: ft.Page, onGuardar, venta: dict = None, errorRef=None) -> ft.AlertDialog:
    esEdicion = venta is not None

    # ── Opciones desde controllers ───────────────────────
    opcionesProductos = [
        ft.dropdown.Option(key=str(p["id"]), text=p["nombre"])
        for p in productosController.obtenerProductos()
    ]
    opcionesPaises = [
        ft.dropdown.Option(key=str(p["id"]), text=f"{p['nombre']} ({p['tipoMoneda']})")
        for p in paisController.obtenerPaises()
    ]

    campoProducto = ft.Dropdown(
        label="Producto",
        value=str(venta["productoId"]) if esEdicion else None,
        options=opcionesProductos if opcionesProductos else [
            ft.dropdown.Option(key="", text="No hay productos registrados")
        ],
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )
    campoPais = ft.Dropdown(
        label="País de venta",
        value=str(venta["paisId"]) if esEdicion else None,
        options=opcionesPaises if opcionesPaises else [
            ft.dropdown.Option(key="", text="No hay países registrados")
        ],
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )
    campoPrecio = ft.TextField(
        label="Precio modificado",
        value=str(venta["precioModificado"]) if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="Precio específico para este país",
        hint_style=ft.TextStyle(color="#3C3C4E"),
        width=320,
    )
    errorTxt = ft.Text("", color=ft.Colors.RED_400, size=12, ref=errorRef)

    def guardar(e):
        errorTxt.value = ""
        errorTxt.update()

        # Validaciones frontend: selección y conversión numérica
        if not campoProducto.value:
            errorTxt.value = "Selecciona un producto."
            errorTxt.update()
            return
        if not campoPais.value:
            errorTxt.value = "Selecciona un país de venta."
            errorTxt.update()
            return
        try:
            precio = float(campoPrecio.value.strip())
        except ValueError:
            errorTxt.value = "El precio debe ser un número (ej: 1500 o 99.99)."
            errorTxt.update()
            return

        # Delegar al controller
        onGuardar({
            "productoId"      : int(campoProducto.value),
            "paisId"          : int(campoPais.value),
            "precioModificado": precio,
        })

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Editar venta" if esEdicion else "Añadir venta",
            color=constants.TEXT_COLOR,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Column(
            tight=True,
            spacing=12,
            controls=[campoProducto, campoPais, campoPrecio, errorTxt],
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
#  Diálogo: Ver venta
# ─────────────────────────────────────────────
def dialogoVer(page: ft.Page, venta: dict) -> ft.AlertDialog:

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
            "Detalle de venta",
            color=constants.TEXT_COLOR,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Column(
            tight=True,
            spacing=10,
            controls=[
                filaDetalle("ID",                venta["id"]),
                filaDetalle("Producto",          venta["nombreProducto"]),
                filaDetalle("País de venta",     venta["nombrePais"]),
                filaDetalle("Moneda",            venta["moneda"]),
                filaDetalle("Precio modificado", f"{venta['precioModificado']:.2f} {venta['moneda']}"),
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
#  Diálogo: Eliminar venta
# ─────────────────────────────────────────────
def dialogoEliminar(page: ft.Page, venta: dict, onConfirmar) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Eliminar venta",
            color=ft.Colors.RED_400,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Text(
            f'¿Estás seguro de eliminar la venta de "{venta["nombreProducto"]}" a {venta["nombrePais"]}?',
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
#  Vista principal de Ventas
# ─────────────────────────────────────────────
def ventas(router) -> ft.Control:

    tablaRef = ft.Ref[ft.DataTable]()

    def construirFilas() -> list[ft.DataRow]:
        datos = ventaController.obtenerVentas()
        if not datos:
            return []

        filas = []
        for i, v in enumerate(datos):
            bgColor = constants.tableRowBg if i % 2 == 0 else constants.tableRowAlt

            def onVer(e, item=v):
                dlg = dialogoVer(router.page, item)
                abrirDialogo(router.page, dlg)

            def onEditar(e, item=v):
                errorRef = ft.Ref[ft.Text]()

                def guardarEdicion(datos):
                    resultado = ventaController.modificarVenta(
                        id               = item["id"],
                        productoId       = datos["productoId"],
                        paisId           = datos["paisId"],
                        precioModificado = datos["precioModificado"],
                    )
                    if isinstance(resultado, str):
                        errorRef.current.value = resultado
                        errorRef.current.update()
                    else:
                        refrescar()
                        cerrarDialogo(router.page, dlg)

                dlg = dialogoVenta(router.page, guardarEdicion, item, errorRef=errorRef)
                abrirDialogo(router.page, dlg)

            def onEliminar(e, item=v):
                def confirmar():
                    ventaController.eliminarVenta(item["id"])
                    refrescar()
                dlg = dialogoEliminar(router.page, item, confirmar)
                abrirDialogo(router.page, dlg)

            filas.append(
                ft.DataRow(
                    color=bgColor,
                    cells=[
                        ft.DataCell(ft.Text(str(v["id"]),                                color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(v["nombreProducto"],                         color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(v["nombrePais"],                             color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(f"{v['precioModificado']:.2f} {v['moneda']}", color=constants.TEXT_COLOR, size=13)),
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
        errorRef = ft.Ref[ft.Text]()

        def guardarNuevo(datos):
            resultado = ventaController.guardarVenta(
                productoId       = datos["productoId"],
                paisId           = datos["paisId"],
                precioModificado = datos["precioModificado"],
            )
            if isinstance(resultado, str):
                errorRef.current.value = resultado
                errorRef.current.update()
            else:
                refrescar()
                cerrarDialogo(router.page, dlg)

        dlg = dialogoVenta(router.page, guardarNuevo, errorRef=errorRef)
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
            ft.DataColumn(ft.Text("Nombre Producto",   color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("País de Venta",     color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Precio Modificado", color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
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
                    "Registro de ventas",
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
                                    ft.Text("Añadir venta", color=constants.btnAddText, weight=ft.FontWeight.W_600),
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

    return layoutPrincipal(router, contenido, activePage="ventas")