import flet as ft
import styles.constants as constants
from views.dashboard import layoutPrincipal
from controller import gmailController, reporteController, usuarioController
from components.uiHelper import abrirDialogo, cerrarDialogo,monedasDisponibles


# ─────────────────────────────────────────────
#  Vista principal de Reporte
# ─────────────────────────────────────────────
def reporte(router) -> ft.Control:

    estadoRef = ft.Ref[ft.Text]()
    subRef    = ft.Ref[ft.Text]()

    # Correo del usuario activo desde el model (sin depender del router)
    sesion        = usuarioController.obtenerSesion()
    correoUsuario = sesion["correo"]   if sesion else "—"
    username      = sesion["username"] if sesion else "—"

    def abrirDialogoEnvio(e):

        # Cargar países en cada apertura
        nombresPaises  = reporteController.obtenerNombresPaises()
        opcionesPaises = [
            ft.dropdown.Option(key=nombre, text=nombre)
            for nombre in nombresPaises
        ]

        campoPais = ft.Dropdown(
            label="País del reporte",
            value=opcionesPaises[0].key if opcionesPaises else None,
            options=opcionesPaises if opcionesPaises else [
                ft.dropdown.Option(key="", text="No hay países registrados")
            ],
            border_color=constants.borderColor,
            focused_border_color=constants.accentColor,
            color=constants.TEXT_COLOR,
            label_style=ft.TextStyle(color="#6C7086"),
            width=320,
        )
        campoMoneda = ft.Dropdown(
            label="Moneda del reporte",
            value="CRC",
            options=monedasDisponibles,
            border_color=constants.borderColor,
            focused_border_color=constants.accentColor,
            color=constants.TEXT_COLOR,
            label_style=ft.TextStyle(color="#6C7086"),
            width=320,
        )
        errorTxt = ft.Text("", color=ft.Colors.RED_400, size=12)

        def onEnviar(e):
            errorTxt.value = ""
            errorTxt.update()

            if not campoPais.value:
                errorTxt.value = "Selecciona un país."
                errorTxt.update()
                return
            if not campoMoneda.value:
                errorTxt.value = "Selecciona una moneda."
                errorTxt.update()
                return

            sesionActual = usuarioController.obtenerSesion()
            if not sesionActual:
                errorTxt.value = "No hay usuario en sesión."
                errorTxt.update()
                return

            resultado = gmailController.enviarReporte(
                correoDestino = sesionActual["correo"],
                nombrePais    = campoPais.value,
                moneda        = campoMoneda.value,
            )

            if isinstance(resultado, str):
                errorTxt.value = resultado
                errorTxt.update()
            else:
                cerrarDialogo(router.page, dlg)
                estadoRef.current.value = f"✓ Reporte enviado correctamente"
                estadoRef.current.color = "#A6E3A1"
                subRef.current.value    = f"{campoPais.value} · {campoMoneda.value} → {sesionActual['correo']}"
                estadoRef.current.update()
                subRef.current.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Enviar reporte por correo",
                color=constants.TEXT_COLOR,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor="#1E1E2E",
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    # ── Destinatario fijo ────────────────────
                    ft.Container(
                        bgcolor="#16213E",
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                        content=ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.MAIL_OUTLINE_ROUNDED, color="#6C7086", size=15),
                                ft.Column(
                                    spacing=1,
                                    tight=True,
                                    controls=[
                                        ft.Text("Destinatario", color="#6C7086", size=10),
                                        ft.Text(correoUsuario,  color=constants.TEXT_COLOR, size=12),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Divider(color=constants.borderColor),
                    campoPais,
                    campoMoneda,
                    errorTxt,
                ],
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: cerrarDialogo(router.page, dlg),
                    style=ft.ButtonStyle(color="#6C7086"),
                ),
                ft.Button(
                    "Generar y enviar",
                    on_click=onEnviar,
                    style=ft.ButtonStyle(
                        bgcolor=constants.btnAddBg,
                        color=constants.btnAddText,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        abrirDialogo(router.page, dlg)

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
                            "Genera y envía el reporte PDF de ventas por país al correo del usuario.",
                            size=13,
                            color="#6C7086",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),

                # ── Info del usuario en sesión ────────────────────
                ft.Container(
                    bgcolor="#1E1E2E",
                    border_radius=10,
                    padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                    content=ft.Row(
                        tight=True,
                        spacing=12,
                        controls=[
                            ft.Container(
                                width=36,
                                height=36,
                                border_radius=18,
                                bgcolor=constants.accentColor,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    username[0].upper() if username != "—" else "?",
                                    color="#121212",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Column(
                                spacing=1,
                                tight=True,
                                controls=[
                                    ft.Text(f"@{username}", color=constants.TEXT_COLOR, size=13, weight=ft.FontWeight.W_500),
                                    ft.Text(f"El reporte se enviará a: {correoUsuario}", color="#6C7086", size=11),
                                ],
                            ),
                        ],
                    ),
                ),

                # ── Estado (aparece tras enviar) ──────────────────
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    controls=[
                        ft.Text(ref=estadoRef, value="", size=13, weight=ft.FontWeight.W_500),
                        ft.Text(ref=subRef,    value="", size=11, color="#6C7086"),
                    ],
                ),

                # ── Botón ─────────────────────────────────────────
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
                    on_click=abrirDialogoEnvio,
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