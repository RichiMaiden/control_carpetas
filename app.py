import flet as ft
from views.inicio_view import pantalla_inicio
from views.mis_carpetas_view import pantalla_mis_carpetas
from views.admin_panel_view import pantalla_admin
from controllers.carpeta_controller import init_db
from controllers.usuario_controller import init_usuarios_db, validar_usuario_login
from controllers.usuario_controller import crear_admin_por_defecto


init_usuarios_db()
crear_admin_por_defecto()

def main(page: ft.Page):
    page.title = "Control de Carpetas"
    page.window_width = 600
    page.window_height = 400
    
    COLOR_FONDO = "#f5f7fa"
    COLOR_TITULO = "#2c3e50"
    COLOR_TEXTO = "#7f8c8d"
    COLOR_BOTON = "#3498db"

    def mostrar_login():
        page.clean()
        usuario_input = ft.TextField(label="Usuario")
        contrasena_input = ft.TextField(label="Contraseña", password=True)
        mensaje = ft.Text()

        def login(e):
            user = usuario_input.value
            pwd = contrasena_input.value
            rol = validar_usuario_login(user, pwd)
            if rol:
                page.clean()
                if rol == "EMPRESA":
                    pantalla_mis_carpetas(page, user, mostrar_inicio)
                elif rol == "ADMIN":
                    pantalla_admin(page, user, mostrar_inicio)
                else:
                    mensaje.value = "Rol no válido para este sistema"
                    page.update()
            else:
                mensaje.value = "Usuario o contraseña incorrectos"
                page.update()

        page.add(
            ft.Column([
                ft.Text("Iniciar Sesión", size=20),
                usuario_input,
                contrasena_input,
                ft.ElevatedButton("Entrar", on_click=login),
                mensaje
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        )

    def mostrar_inicio():
        pantalla_inicio(page, mostrar_login)

    mostrar_inicio()

ft.app(target=main)
