import flet as ft

import styles.constants as constants
import router.routing as routing
def view_bienvenida(on_empezar) -> ft.Control:
    """
    Vista inicial con el nombre del sistema centrado
    y un botón 'Empezar' justo debajo.
    """
    return ft.Container(
        expand=True,
        bgcolor=constants.BG_COLOR,
        alignment=ft.Alignment.CENTER,          
        content=ft.Column(
            tight=True,                          
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=36,                          
            controls=[

                # ── Título del sistema ──────────────────────────
                ft.Text(
                    "ATI Logistica Aduanera S.A 🚚",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=constants.TEXT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),

                
                ft.Button(
                    content=ft.Text("Empezar"),
                    on_click=on_empezar,
                    style=ft.ButtonStyle(
                        bgcolor={
                        ft.ControlState.DEFAULT: constants.BTN_BG,   # color normal
                        ft.ControlState.HOVERED: "#CBA6F7",   
                        },
                        color={
                            ft.ControlState.DEFAULT: constants.BTN_TEXT,   # texto normal
                            ft.ControlState.HOVERED: "#FFFFFF",  
                        },
                        padding=ft.Padding.symmetric(vertical=14, horizontal=48),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        text_style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.W_600,
                        ),
                        
                    ),
                ),

            ],
        ),
    )



def main(page: ft.Page):
    # Configuración general de la ventana
    page.title         = "ATI Logistica Aduanera S.A"
    page.bgcolor       = constants.BG_COLOR
    page.theme_mode    = ft.ThemeMode.DARK
    page.window.width  = 1024
    page.window.height = 680
    page.window.min_width  = 800
    page.window.min_height = 500
    page.padding = 0

    # ── Manejador de navegación entre vistas ────────────

        

    # ── Cargar vista inicial ─────────────────────────────
    page.add(view_bienvenida(on_empezar=lambda e: routing.navegarLogin(page)))



ft.run(main)

