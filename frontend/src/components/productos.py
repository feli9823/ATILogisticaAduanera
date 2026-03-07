import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal


# ─────────────────────────────────────────────
#  Datos en memoria
# ─────────────────────────────────────────────
listaProductos: list[dict] = []
nextId = 1


# ─────────────────────────────────────────────
#  Utilidades para manejo de diálogos
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
#  Diálogo: Añadir / Editar
# ─────────────────────────────────────────────
def dialogoProducto(page: ft.Page, onGuardar, producto: dict = None) -> ft.AlertDialog:
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
    errorTxt = ft.Text("", color=ft.Colors.RED_400, size=12)

    def guardar(e):
        if not campoNombre.value.strip():
            errorTxt.value = "El nombre es obligatorio."
            errorTxt.update()
            return
        if not campoPrecio.value.strip():
            errorTxt.value = "El precio es obligatorio."
            errorTxt.update()
            return
        try:
            precio = float(campoPrecio.value.strip())
        except ValueError:
            errorTxt.value = "El precio debe ser un número."
            errorTxt.update()
            return

        onGuardar({
            "nombre": campoNombre.value.strip(),
            "precio": precio,
           
        })
        cerrarDialogo(page, dlg)

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
            controls=[campoNombre, campoPrecio,  errorTxt],
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

    def filaDetalle(label, valor):
        return ft.Row(
            controls=[
                ft.Text(label, color="#6C7086", size=13, width=140),
                ft.Text(str(valor), color=constants.TEXT_COLOR, size=13),
            ],
        )

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
                filaDetalle("ID",                  producto["id"]),
                filaDetalle("Nombre",              producto["nombre"]),
                filaDetalle("Precio base",         f" ₡ {producto['precio']}"),
                
            ],
        ),
        actions=[
            ft.TextButton(
                "Cerrar",
                on_click=lambda e: cerrarDialogo(page, dlg),
                style=ft.ButtonStyle(color=constants.   accentColor),
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
    global nextId

    tablaRef = ft.Ref[ft.DataTable]()

    def construirFilas() -> list[ft.DataRow]:
        if not listaProductos:
            return []

        filas = []
        for i, p in enumerate(listaProductos):
            bgColor = constants.tableRowBg if i % 2 == 0 else constants.tableRowAlt

            def onVer(e, prod=p):
                dlg = dialogoVer(router.page, prod)
                abrirDialogo(router.page, dlg)

            def onEditar(e, prod=p):
                def guardarEdicion(datos):
                    prod["nombre"] = datos["nombre"]
                    prod["precio"] = datos["precio"]
                    
                    refrescar()
                dlg = dialogoProducto(router.page, guardarEdicion, prod)
                abrirDialogo(router.page, dlg)

            def onEliminar(e, prod=p):
                def confirmar():
                    listaProductos.remove(prod)
                    refrescar()
                dlg = dialogoEliminar(router.page, prod, confirmar)
                abrirDialogo(router.page, dlg)

            filas.append(
                ft.DataRow(
                    color=bgColor,
                    cells=[
                        ft.DataCell(ft.Text(str(p["id"]),          color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(p["nombre"],           color=constants.TEXT_COLOR, size=13)),
                        ft.DataCell(ft.Text(f" ₡ {p['precio']}", color=constants.TEXT_COLOR, size=13)),
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
            listaProductos.append({
                "id"    : nextId,
                "nombre": datos["nombre"],
                "precio": datos["precio"],
            })
            nextId += 1
            refrescar()

        dlg = dialogoProducto(router.page, guardarNuevo)
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
            ft.DataColumn(ft.Text("ID",                  color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Nombre",              color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Precio en colones",              color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
            ft.DataColumn(ft.Text("Acciones",            color=constants.accentColor, weight=ft.FontWeight.BOLD, size=13)),
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