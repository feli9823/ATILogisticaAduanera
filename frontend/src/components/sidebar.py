import flet as ft
import styles.constants as constants
from controller import usuarioController
from shared import session

SIDEBAR_BG    = "#1A1A2E"
ITEM_HOVER    = "#2A2A3E"
ITEM_ACTIVE   = "#CBA6F7"
ITEM_TEXT     = "#CDD6F4"
ICON_INACTIVE = "#6C7086"
SIDEBAR_WIDTH = 220


def _on_hover(e):
    e.control.bgcolor = ITEM_HOVER if e.data == "true" else SIDEBAR_BG
    e.control.update()


def _sidebar_item(label, icon, active, on_click) -> ft.Control:
    color      = ITEM_ACTIVE if active else ITEM_TEXT
    icon_color = ITEM_ACTIVE if active else ICON_INACTIVE

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=icon_color, size=20),
                ft.Text(label, color=color, size=14, weight=ft.FontWeight.W_500),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        border_radius=8,
        on_click=on_click,
        bgcolor=SIDEBAR_BG,
        ink=True,
        on_hover=_on_hover,
    )

def _usuario_widget(router) -> ft.Control:
    """
    Widget inferior del sidebar que muestra la sesión activa.
    Al pasar el mouse aparece un tooltip con ID, username y correo.
    """
    sesion = session.obtener() 
    if not sesion:
        return ft.Container()

    username = sesion["username"]
    correo   = sesion["correo"]
    uid      = sesion["id"]
    inicial  = username[0].upper()

    # El tooltip se asigna como propiedad del Container, no como wrapper
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        border_radius=8,
        bgcolor=SIDEBAR_BG,
        tooltip=f"ID: {uid}  |  @{username}\n{correo}",
        on_hover=lambda e: (
            setattr(e.control, "bgcolor", ITEM_HOVER if e.data == "true" else SIDEBAR_BG),
            e.control.update()
        ),
        content=ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # ── Avatar circular ──────────────────────────
                ft.Container(
                    width=34,
                    height=34,
                    border_radius=17,
                    bgcolor=ITEM_ACTIVE,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        inicial,
                        color="#121212",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                # ── Username y correo ────────────────────────
                ft.Column(
                    spacing=1,
                    tight=True,
                    controls=[
                        ft.Text(
                            f"{username}",
                            color=ITEM_TEXT,
                            size=13,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            correo,
                            color=ICON_INACTIVE,
                            size=10,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            max_lines=1,
                            width=130,
                        ),
                    ],
                ),
            ],
        ),
    )



class Sidebar:
    """
    Sidebar con animación de entrada/salida.
    Uso:
        sb = Sidebar(router, active_page="productos")
        page.add(sb.build())
        sb.toggle()   ← para abrir/cerrar
    """

    def __init__(self, router, active_page: str = "productos"):
        self.router      = router
        self.active_page = active_page
        self._visible    = True        # estado actual

        nav_items = [
            {
                "label": "Productos",
                "icon" : ft.Icons.INVENTORY_2_OUTLINED,
                "key"  : "productos",
                "action": lambda e: router.navegarProductos(),
            },
            {
                "label": "País",
                "icon" : ft.Icons.PUBLIC_OUTLINED,
                "key"  : "pais",
                "action": lambda e: router.navegarPais(),
            },
            {
                "label": "Ventas",
                "icon" : ft.Icons.ATTACH_MONEY,
                "key"  : "ventas",
                "action": lambda e: router.navegarVentas(),
            },

            {
                "label": "Consultas de ventas",
                "icon" : ft.Icons.QUESTION_MARK,
                "key"  : "consultas_ventas",
                "action": lambda e: router.navegarConsultasVentas(),
            },

            {
                "label": "Reporte",
                "icon" : ft.Icons.BAR_CHART_OUTLINED,
                "key"  : "reporte",
                "action": lambda e: router.navegarReporte(),
            },
        ]

        # ── Contenedor animado ───────────────────────────────
        self.container = ft.Container(
            width=SIDEBAR_WIDTH,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            bgcolor=SIDEBAR_BG,
            padding=ft.Padding.symmetric(vertical=24, horizontal=8),

            
            animate=ft.Animation(        # ← animación del ancho
                duration=300,
                curve=ft.AnimationCurve.EASE_IN_OUT,
            ),

            content=ft.Column(
                expand=True,
                spacing=4,
                controls=[

                    # ── Logo ────────────────────────────────
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.Icons.LOCAL_SHIPPING_OUTLINED,
                                    color=ITEM_ACTIVE,
                                    size=32,
                                ),
                                ft.Text(
                                    "ATI Logística",
                                    color=constants.TEXT_COLOR,
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                        ),
                        padding=ft.Padding.only(bottom=24),
                        alignment=ft.Alignment.CENTER,
                    ),

                    ft.Divider(color="#2A2A3E", height=1),
                    ft.Container(height=12),

                    # ── Items ────────────────────────────────
                    *[
                        _sidebar_item(
                            label=item["label"],
                            icon=item["icon"],
                            active=(active_page == item["key"]),
                            on_click=item["action"],
                        )
                        for item in nav_items
                    ],

                    ft.Container(expand=True),

                    ft.Divider(color="#2A2A3E", height=1),

                    # ── Widget de sesión activa ──────────────────
                    _usuario_widget(router),

                ],
            ),
        )

    def build(self) -> ft.Control:
        """Retorna el widget listo para agregar a la página."""
        return self.container

    def toggle(self):
        """Alterna entre mostrar y ocultar el sidebar con animación."""
        if self._visible:
            self.container.width  = 0   
        else:

            self.container.width  = SIDEBAR_WIDTH

        self._visible = not self._visible
        self.container.update()