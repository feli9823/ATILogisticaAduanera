import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal
import controller.paisController as paisController
from components.uiHelper import abrirDialogo, cerrarDialogo, filaDetalle,monedasDisponibles

# ─────────────────────────────────────────────
#  Monedas disponibles (RF-13)
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
#  Diálogo: Añadir / Editar país
# ─────────────────────────────────────────────
def dialogoPais(page: ft.Page, onGuardar, paisItem: dict = None, errorRef=None) -> ft.AlertDialog:
    esEdicion = paisItem is not None

    campoNombre = ft.TextField(
        label="Nombre del país",
        value=paisItem["nombre"] if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )
    campoImpuesto = ft.TextField(
        label="Tarifa de impuesto (%)",
        value=str(paisItem["tarifaImpuesto"]) if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=320,
    )
    campoMoneda = ft.Dropdown(
        label="Moneda",
        value=paisItem["tipoMoneda"] if esEdicion else "USD",
        options=monedasDisponibles,
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )

    # errorTxt vinculado al ref externo para que onGuardar pueda actualizarlo
    errorTxt = ft.Text("", color=ft.Colors.RED_400, size=12, ref=errorRef)

    def guardar(e):
        # Limpiar error previo
        errorTxt.value = ""
        errorTxt.update()

        # Única validación en el frontend: conversión de string a float
        try:
            impuesto = float(campoImpuesto.value.strip())
        except ValueError:
            errorTxt.value = "La tarifa debe ser un número (ej: 13 o 13.5)."
            errorTxt.update()
            return

        # Delegar todo lo demás al controller via onGuardar
        onGuardar({
            "nombre"         : campoNombre.value.strip(),
            "tarifaImpuesto" : impuesto,
            "tipoMoneda"     : campoMoneda.value or "USD",
        })

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
def dialogoVer(page: ft.Page, paisItem: dict) -> ft.AlertDialog:

    

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
                filaDetalle("ID",              paisItem["id"]),
                filaDetalle("Nombre",          paisItem["nombre"]),
                filaDetalle("Tarifa impuesto", f"{paisItem['tarifaImpuesto']}%"),
                filaDetalle("Moneda",          paisItem["tipoMoneda"]),
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
def dialogoEliminar(page: ft.Page, paisItem: dict, onConfirmar) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Eliminar país",
            color=ft.Colors.RED_400,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Text(
            f'¿Estás seguro de eliminar "{paisItem["nombre"]}"?',
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

    tablaRef = ft.Ref[ft.DataTable]()

    def construirFilas() -> list[ft.DataRow]:
        datos = paisController.obtenerPaises()
        if not datos:
            return []

        filas = []
        for i, p in enumerate(datos):
            bgColor = constants.tableRowBg if i % 2 == 0 else constants.tableRowAlt

            def onVer(e, item=p):
                dlg = dialogoVer(router.page, item)
                abrirDialogo(router.page, dlg)

            def onEditar(e, item=p):
                errorRef = ft.Ref[ft.Text]()

                def guardarEdicion(datos):
                    resultado = paisController.modificarPais(
                        id=item["id"],
                        nombre=datos["nombre"],
                        tarifaImpuesto=datos["tarifaImpuesto"],
                        tipoMoneda=datos["tipoMoneda"],
                    )
                    if isinstance(resultado, str):
                        # Error del controller → mostrar en el diálogo
                        errorRef.current.value = resultado
                        errorRef.current.update()
                    else:
                        refrescar()
                        cerrarDialogo(router.page, dlg)

                dlg = dialogoPais(router.page, guardarEdicion, item, errorRef=errorRef)
                abrirDialogo(router.page, dlg)

            def onEliminar(e, item=p):
                def confirmar():
                    paisController.eliminarPais(item["id"])
                    refrescar()
                dlg = dialogoEliminar(router.page, item, confirmar)
                abrirDialogo(router.page, dlg)

            filas.append(
                ft.DataRow(
                    color=bgColor,
                    cells=[
                        ft.DataCell(ft.Text(str(p["id"]),              color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(p["nombre"],               color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(f"{p['tarifaImpuesto']}%", color=constants.TEXT_COLOR, size=13)),
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
            resultado = paisController.guardarPais(
                nombre=datos["nombre"],
                tarifaImpuesto=datos["tarifaImpuesto"],
                tipoMoneda=datos["tipoMoneda"],
            )
            if isinstance(resultado, str):
                # Error del controller → mostrar en el diálogo sin cerrarlo
                errorRef.current.value = resultado
                errorRef.current.update()
            else:
                # Éxito → refrescar tabla y cerrar
                refrescar()
                cerrarDialogo(router.page, dlg)

        dlg = dialogoPais(router.page, guardarNuevo, errorRef=errorRef)
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
            ft.DataColumn(ft.Text("ID",              color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Nombre País",     color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Tarifa Impuesto", color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Acciones",        color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
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