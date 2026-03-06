import flet as ft
from views import loginUser
def navegar(page: ft.Page, e):
    page.controls.clear()  # Limpia la vista actual
    page.add(e)  # Carga la vista de login de usuario
    page.update()

def navegarLogin(page: ft.Page):
    navegar(page, loginUser.loginUser())


def dashboard(page: ft.Page, e):
    print("Dashboard")