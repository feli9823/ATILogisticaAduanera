import flet as ft

import styles.constants as constants

def abrirDialogo(page: ft.Page, dlg: ft.AlertDialog) -> None:
    if dlg not in page.overlay:
        page.overlay.append(dlg)
    dlg.open = True
    page.update()

def cerrarDialogo(page: ft.Page, dlg: ft.AlertDialog) -> None:
    dlg.open = False
    page.update()

monedasDisponibles = [
    ft.dropdown.Option(key="CRC", text="₡ Colones (CRC)"),
    ft.dropdown.Option(key="USD", text="$ Dólares (USD)"),
    ft.dropdown.Option(key="EUR", text="€ Euros (EUR)"),
    ft.dropdown.Option(key="BRL", text="R$ Reales Brasileños (BRL)"),
]


def filaDetalle(label, valor):
        return ft.Row(
            controls=[
                ft.Text(label, color="#6C7086", size=13, width=140),
                ft.Text(str(valor), color=constants.TEXT_COLOR, size=13),
            ],
        )