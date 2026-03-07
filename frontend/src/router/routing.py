import flet as ft
from views import loginUser, dashboard
from components import productos, pais, reporte, ventas , consultasVentas

class Router:
    def __init__(self, page: ft.Page):
        self.page = page

    def navegar(self, vista: ft.Control):
        self.page.controls.clear()  # Limpia la vista actual
        self.page.add(vista)  # Carga la vista especificada
        self.page.update()

    def navegarLogin(self):
        self.navegar(loginUser.loginUser(self))


    def navegarDashboard(self):
        self.navegar(dashboard.dashboard(self))
        
    def navegarProductos(self):
        self.navegar(productos.productos(self))

    def navegarPais(self):
        self.navegar(pais.pais(self))

    def navegarReporte(self):
        self.navegar(reporte.reporte(self))

    def navegarVentas(self):
        self.navegar(ventas.ventas(self))

    def consultasVentas(self):
        self.navegar(consultasVentas.consultasVentas(self))


