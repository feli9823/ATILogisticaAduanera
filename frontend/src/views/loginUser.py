import flet as ft
import styles.constants as constants

def loginUser():
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
                    "Login de Usuario",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=constants.TEXT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),

            ],
        ),
    )

