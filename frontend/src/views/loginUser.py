import flet as ft
import styles.constants as constants

def loginUser(router) -> ft.Control:
    labelTextColor= '#333333'
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
                    "Inicie sesion",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=constants.TEXT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),

                # ── Formulario de login ───────────────────────────
                ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                    controls=[
                        ft.TextField(
                            label="Usuario",
                            width=300,
                            border_color=labelTextColor,
                            focused_border_color=constants.BG_COLOR,
                        ),
                        ft.TextField(
                            label="Correo Electrónico",
                            width=300,
                            border_color=labelTextColor,
                            focused_border_color=constants.BG_COLOR,
                            
                        ),
                        ft.Button(
                            content=ft.Text("Iniciar Sesión"),
                            on_click=lambda e: router.navegarDashboard(),
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.DEFAULT: constants.BTN_BG,
                                    ft.ControlState.HOVERED: "#CBA6F7",
                                },
                                color={
                                    ft.ControlState.DEFAULT: constants.BTN_TEXT,
                                    ft.ControlState.HOVERED: "#FFFFFF",
                                },
                                padding=ft.Padding.symmetric(vertical=14, horizontal=48),
                                shape=ft.RoundedRectangleBorder(radius=8),
                                text_style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                ),
                            ),
                            width=300,
                        ),
                    ],
                )

            ],
        ),
    )

