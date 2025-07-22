import flet as ft
from controllers.usuario_controller import agregar_usuario, obtener_usuarios, eliminar_usuario
from controllers.carpeta_controller import obtener_todas_las_carpetas, exportar_carpetas_a_csv

COLOR_FONDO = "#f5f7fa"
COLOR_TITULO = "#2c3e50"
COLOR_BOTON = "#3498db"
COLOR_BOTON_ELIMINAR = "#e74c3c"

def pantalla_admin(page: ft.Page, usuario_admin: str, funcion_mostrar_inicio):
    page.clean()
    page.title = "Panel de Administrador"

    lista_usuarios = ft.Column(spacing=5)

    def cerrar_dialogo(dlg):
        dlg.open = False
        page.update()

    def actualizar_lista_usuarios():
        lista_usuarios.controls.clear()
        for id_usuario, usuario, rol in obtener_usuarios():
            def borrar_usuario(e, idu=id_usuario, user=usuario):
                eliminar_usuario(idu)
                page.snack_bar = ft.SnackBar(ft.Text(f"Usuario '{usuario}' eliminado."), open=True)
                page.update
                actualizar_lista_usuarios()

            lista_usuarios.controls.append(
                ft.Row([
                    ft.Text(f"{usuario} — Rol: {rol}"),
                    ft.ElevatedButton("Eliminar", on_click=borrar_usuario, style=ft.ButtonStyle(color="red"))
                ], spacing=10)
            )
        page.update()

    usuario_input = ft.TextField(label="Usuario")
    contrasena_input = ft.TextField(label="Contraseña", password=True)
    rol_input = ft.Dropdown(
        label="Rol",
        options=[
            ft.dropdown.Option("ADMIN"),
            ft.dropdown.Option("EMPRESA")
        ]
    )

    def agregar_usuario_evento(e):
        if usuario_input.value and contrasena_input.value and rol_input.value:
            agregar_usuario(usuario_input.value, contrasena_input.value, rol_input.value)
            page.snack_bar = ft.SnackBar(ft.Text("Usuario agregado exitosamente."), open=True)
            usuario_input.value = ""
            contrasena_input.value = ""
            rol_input.value = ""
            actualizar_lista_usuarios()

    def mostrar_todas_las_carpetas(e):
        lista = []

        for id_carpeta, usuario, licitacion, detalle, estado in obtener_todas_las_carpetas():
            lista.append(
            ft.Text(f"ID: {id_carpeta} — Usuario: {usuario} — Licitación: {licitacion} — Detalle: {detalle} — Estado: {estado}")
        )

        contenido = ft.Column(lista, scroll=ft.ScrollMode.ALWAYS, height=300)

        dlg = ft.AlertDialog(
            title=ft.Text("Listado de Todas las Carpetas"),
            content=contenido,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dlg))
        ],
        scrollable=True
    )

        page.dialog = dlg
        dlg.open = True
        page.update()

    def exportar_csv_evento(e):
        exportar_carpetas_a_csv()
        page.snack_bar = ft.SnackBar(ft.Text("CSV exportado exitosamente."), open=True)
        page.update()

    page.add(
        ft.Text(f"Bienvenido {usuario_admin} — Panel de Administración", size=20),
        usuario_input,
        contrasena_input,
        rol_input,
        ft.Row([
            ft.ElevatedButton("Agregar Usuario", on_click=agregar_usuario_evento),
            ft.ElevatedButton("Ver Todas las Carpetas", on_click=mostrar_todas_las_carpetas),
            ft.ElevatedButton("Exportar Carpetas a CSV", on_click=exportar_csv_evento)
        ], spacing=10),
        ft.Divider(),
        ft.Text("Listado de Usuarios:"),
        lista_usuarios,
        ft.Divider(),
        ft.ElevatedButton("Cerrar sesión", on_click=lambda e: funcion_mostrar_inicio())
    )
    actualizar_lista_usuarios()