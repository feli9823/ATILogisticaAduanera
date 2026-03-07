import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal


def reporte(router) -> ft.Control:

    def onEnviarCorreo(e):
        # TODO: implementar lógica de envío de reporte por correo
        print("[REPORTE] Enviar al correo solicitado")

    contenido = ft.Container(
        expand=True,
        bgcolor=constants.BG_COLOR,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=32,
            controls=[

                # ── Título ───────────────────────────────────────
                ft.Column(
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            ft.Icons.BAR_CHART_ROUNDED,
                            color=constants.accentColor,
                            size=48,
                        ),
                        ft.Text(
                            "Reporte de ventas",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=constants.TEXT_COLOR,
                        ),
                        ft.Text(
                            "Genera y envía el reporte de ventas por correo electrónico.",
                            size=13,
                            color="#6C7086",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),

                # ── Botón enviar ─────────────────────────────────
                ft.Button(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.MAIL_OUTLINE_ROUNDED, color=constants.btnAddText, size=20),
                            ft.Text(
                                "Enviar al correo",
                                color=constants.btnAddText,
                                weight=ft.FontWeight.W_600,
                                size=15,
                            ),
                        ],
                        spacing=10,
                        tight=True,
                    ),
                    on_click=onEnviarCorreo,
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.ControlState.DEFAULT: constants.btnAddBg,
                            ft.ControlState.HOVERED: "#A78BDA",
                        },
                        color=constants.btnAddText,
                        padding=ft.Padding.symmetric(vertical=16, horizontal=40),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),

            ],
        ),
    )

    return layoutPrincipal(router, contenido, activePage="reporte")