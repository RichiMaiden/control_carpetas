import flet as ft

# 🎨 Paleta de colores corporativos
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
        src="https://imgur.com/a/BQPYl5e",
        width=300,
        height=150,
        fit=ft.ImageFit.CONTAIN
    )

    contenido = ft.Column(
        [
            ft.Text("Bienvenido a OK Computer", size=24, weight="bold", color=COLOR_TITULO),
            ft.Text("Soluciones digitales para un futuro innovador", italic=True, color=COLOR_TEXTO),
            logo,
            ft.ElevatedButton(
                "Iniciar sesión",
                on_click=lambda e: funcion_ir_login(),
                style=ft.ButtonStyle(bgcolor=COLOR_BOTON, color="white")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Container(
            contenido,
            alignment=ft.alignment.center,
            bgcolor=COLOR_FONDO,
            expand=True
        )
    )
