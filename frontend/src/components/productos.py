import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal
from controller import productosController
from components.uiHelper import abrirDialogo, cerrarDialogo, filaDetalle
# ─────────────────────────────────────────────
#  Diálogo: Añadir / Editar
# ─────────────────────────────────────────────
def dialogoProducto(page: ft.Page, onGuardar, producto: dict = None, errorRef=None) -> ft.AlertDialog:
    esEdicion = producto is not None

    campoNombre = ft.TextField(
        label="Nombre del producto",
        value=producto["nombre"] if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        width=320,
    )
    campoPrecio = ft.TextField(
        label="Precio base",
        value=str(producto["precio"]) if esEdicion else "",
        border_color=constants.borderColor,
        focused_border_color=constants.accentColor,
        color=constants.TEXT_COLOR,
        label_style=ft.TextStyle(color="#6C7086"),
        keyboard_type=ft.KeyboardType.NUMBER,
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
            precio = float(campoPrecio.value.strip())
        except ValueError:
            errorTxt.value = "El precio debe ser un número (ej: 1500 o 99.99)."
            errorTxt.update()
            return

        # Delegar todo lo demás al controller via onGuardar
        onGuardar({
            "nombre": campoNombre.value.strip(),
            "precio": precio,
        })

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Editar producto" if esEdicion else "Añadir producto",
            color=constants.TEXT_COLOR,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Column(
            tight=True,
            spacing=12,
            controls=[campoNombre, campoPrecio, errorTxt],
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
#  Diálogo: Ver
# ─────────────────────────────────────────────
def dialogoVer(page: ft.Page, producto: dict) -> ft.AlertDialog:

    

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Detalle del producto",
            color=constants.TEXT_COLOR,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Column(
            tight=True,
            spacing=10,
            controls=[
                filaDetalle("ID",          producto["id"]),
                filaDetalle("Nombre",      producto["nombre"]),
                filaDetalle("Precio base", f"₡ {producto['precio']}"),
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
#  Diálogo: Eliminar
# ─────────────────────────────────────────────
def dialogoEliminar(page: ft.Page, producto: dict, onConfirmar) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Eliminar producto",
            color=ft.Colors.RED_400,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1E1E2E",
        content=ft.Text(
            f'¿Estás seguro de eliminar "{producto["nombre"]}"?',
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
#  Vista principal de Productos
# ─────────────────────────────────────────────
def productos(router) -> ft.Control:

    tablaRef = ft.Ref[ft.DataTable]()

    def construirFilas() -> list[ft.DataRow]:
        datos = productosController.obtenerProductos()
        if not datos:
            return []

        filas = []
        for i, p in enumerate(datos):
            bgColor = constants.tableRowBg if i % 2 == 0 else constants.tableRowAlt

            def onVer(e, prod=p):
                dlg = dialogoVer(router.page, prod)
                abrirDialogo(router.page, dlg)

            def onEditar(e, prod=p):
                errorRef = ft.Ref[ft.Text]()

                def guardarEdicion(datos):
                    resultado = productosController.modificarProducto(
                        id=prod["id"],
                        nombre=datos["nombre"],
                        precio=datos["precio"],
                    )
                    if isinstance(resultado, str):
                        # Error del controller → mostrar en el diálogo
                        errorRef.current.value = resultado
                        errorRef.current.update()
                    else:
                        refrescar()
                        cerrarDialogo(router.page, dlg)

                dlg = dialogoProducto(router.page, guardarEdicion, prod, errorRef=errorRef)
                abrirDialogo(router.page, dlg)

            def onEliminar(e, prod=p):
                def confirmar():
                    productosController.eliminarProducto(prod["id"])
                    refrescar()
                dlg = dialogoEliminar(router.page, prod, confirmar)
                abrirDialogo(router.page, dlg)

            filas.append(
                ft.DataRow(
                    color=bgColor,
                    cells=[
                        ft.DataCell(ft.Text(str(p["id"]),        color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(p["nombre"],         color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(f"₡ {p['precio']}", color=constants.TEXT_COLOR, size=13)),
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
            resultado = productosController.guardarProducto(
                nombre=datos["nombre"],
                precio=datos["precio"],
            )
            if isinstance(resultado, str):
                # Error del controller → mostrar en el diálogo sin cerrarlo
                errorRef.current.value = resultado
                errorRef.current.update()
            else:
                # Éxito → refrescar tabla y cerrar
                refrescar()
                cerrarDialogo(router.page, dlg)

        dlg = dialogoProducto(router.page, guardarNuevo, errorRef=errorRef)
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
            ft.DataColumn(ft.Text("Nombre",            color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Precio en colones", color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
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
                    "Lista de productos",
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
                                    ft.Text("Añadir producto", color=constants.btnAddText, weight=ft.FontWeight.W_600),
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

    return layoutPrincipal(router, contenido, activePage="productos")   