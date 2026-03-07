import flet as ft
import styles.constants as constants
from components.sidebar import Sidebar


def layoutPrincipal(router, contenido: ft.Control, activePage: str = "dashboard") -> ft.Control:
    """
    Layout reutilizable que incluye el sidebar y el botón hamburguesa.
    """
    sb = Sidebar(router, active_page=activePage)

    def toggle_sidebar(e):
        sb.toggle()

    return ft.Row(
        expand=True,
        spacing=0,
        controls=[

            # ── Sidebar animado ──────────────────────────
            sb.build(),

            # ── Área derecha ─────────────────────────────
            ft.Column(
                expand=True,
                spacing=0,
                controls=[

                    # ── Botón hamburguesa ────────────────
                    ft.Container(
                        bgcolor=constants.BG_COLOR,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.MENU,
                                    icon_color=constants.TEXT_COLOR,
                                    on_click=toggle_sidebar,
                                    tooltip="Menú",
                                ),
                            ],
                        ),
                    ),

                    # ── Contenido dinámico de cada vista ──
                    contenido,

                ],
            ),

        ],
    )


# ─────────────────────────────────────────────
#  Vista Dashboard
# ─────────────────────────────────────────────
def dashboard(router) -> ft.Control:
    contenido = ft.Container(
        expand=True,
        bgcolor=constants.BG_COLOR,
        padding=ft.Padding.all(32),
        content=ft.Text(
            "Dashboard",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=constants.TEXT_COLOR,
        ),
    )
    return layoutPrincipal(router, contenido, activePage="dashboard")