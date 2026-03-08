import flet as ft
import styles.constants as constants
import controller.usuarioController as usuarioController


def loginUser(router) -> ft.Control:
    labelTextColor = "#333333"

    campoUsuario = ft.TextField(
        label="Usuario",
        width=300,
        border_color=labelTextColor,
        focused_border_color=constants.accentColor,
    )
    campoCorreo = ft.TextField(
        label="Correo Electrónico",
        width=300,
        border_color=labelTextColor,
        focused_border_color=constants.accentColor,
    )
    errorTxt = ft.Text("", color=ft.Colors.RED_400, size=12)

    def onIngresar(e):
        # Limpiar error previo
        errorTxt.value = ""
        errorTxt.update()

        # Validación frontend: campos no vacíos
        if not campoUsuario.value.strip():
            errorTxt.value = "El campo usuario es obligatorio."
            errorTxt.update()
            return
        if not campoCorreo.value.strip():
            errorTxt.value = "El campo correo es obligatorio."
            errorTxt.update()
            return

        # Delegar al controller — registra o valida según el caso
        resultado = usuarioController.ingresar(
            username=campoUsuario.value.strip(),
            correo=campoCorreo.value.strip(),
        )

        if isinstance(resultado, str):
            # Error del controller → mostrar en pantalla sin navegar
            errorTxt.value = resultado
            errorTxt.update()
        else:
            # Éxito (registro nuevo o acceso existente) → navegar
            router.navegarDashboard()

    return ft.Container(
        expand=True,
        bgcolor=constants.BG_COLOR,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=36,
            controls=[

                ft.Text(
                    "Inicie sesión",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=constants.TEXT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                    controls=[
                        campoUsuario,
                        campoCorreo,
                        errorTxt,
                        ft.Button(
                            content=ft.Text("Ingresar"),
                            on_click=onIngresar,
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
                ),

            ],
        ),
    )