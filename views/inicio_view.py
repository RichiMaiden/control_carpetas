import flet as ft

# 🎨 Paleta de colores
COLOR_FONDO = "#f5f7fa"
COLOR_TITULO = "#2c3e50"
COLOR_TEXTO = "#7f8c8d"
COLOR_BOTON = "#3498db"

def pantalla_inicio(page: ft.Page, funcion_ir_login):
    page.clean()
    page.title = "Inicio — OK Computer"
    page.window_width = 600
    page.window_height = 400

    logo = ft.Image(
        src="https://i.imgur.com/BQPYl5e",
        width=300,
        height=150,
        fit=ft.ImageFit.CONTAIN
    )

    contenido = ft.Column(
        [
            ft.Text("Bienvenido al Sistema de Gestión Carpetas", size=24, weight="bold"),
            ft.Text("Cargado con la energia de Ok Computer Caacupé:", italic=True, size=20),
            logo,
            ft.ElevatedButton("Iniciar sesión", on_click=lambda e: funcion_ir_login())
        ],
        alignment=ft.MainAxisAlignment.CENTER,         # Centrado vertical
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal
        spacing=20
    )

    page.add(
        ft.Container(
            contenido,
            alignment=ft.alignment.center,  # Centrado general en el contenedor
            expand=True                     # Ocupa toda la ventana para centrar bien
        )
    )
