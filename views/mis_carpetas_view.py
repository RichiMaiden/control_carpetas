import flet as ft
from controllers.carpeta_controller import agregar_carpeta, obtener_carpetas_por_usuario, actualizar_estado_carpeta, eliminar_carpeta, obtener_historial_por_carpeta

COLOR_FONDO = "#f5f7fa"
COLOR_TITULO = "#2c3e50"
COLOR_BOTON = "#3498db"
COLOR_BOTON_ELIMINAR = "#e74c3c"

def pantalla_mis_carpetas(page: ft.Page, usuario: str, funcion_mostrar_inicio):
    page.clean()
    page.title = "Mis Carpetas"

    lista_carpetas = ft.Column()

    def actualizar_lista():
        lista_carpetas.controls.clear()
        for id, licitacion, detalle, estado in obtener_carpetas_por_usuario(usuario):
            estado_dropdown = ft.Dropdown(
                value=estado,
                width=150,
                options=[
                    ft.dropdown.Option("Enviada"),
                    ft.dropdown.Option("En Revisión"),
                    ft.dropdown.Option("Aprobada"),
                    ft.dropdown.Option("Rechazada")
                ]
            )

            def cambiar_estado(e, id_carpeta=id, dropdown=estado_dropdown):
                actualizar_estado_carpeta(id_carpeta, dropdown.value)
                actualizar_lista()

            def borrar_carpeta(e, id_carpeta=id):
                eliminar_carpeta(id_carpeta)
                actualizar_lista()

            def ver_historial(e, id_carpeta=id):
                historial = obtener_historial_por_carpeta(id_carpeta)
                historial_texto = "\n".join(
                    [f"{accion} — {detalle} ({fecha})" for accion, detalle, fecha in historial]
                ) or "Sin historial registrado."

                dlg = ft.AlertDialog(
                    title=ft.Text("Historial de Cambios"),
                    content=ft.Text(historial_texto),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: dlg.close())],
                )
                page.dialog = dlg
                dlg.open = True
                page.update()

            lista_carpetas.controls.append(
                ft.Column([
                    ft.Row([
                        ft.Text(f"Licitación: {licitacion} — {detalle} — Estado:"),
                        estado_dropdown,
                        ft.ElevatedButton("Cambiar Estado", on_click=cambiar_estado),
                        ft.ElevatedButton("Eliminar", on_click=borrar_carpeta, style=ft.ButtonStyle(color="red")),
                        ft.ElevatedButton("Ver Historial", on_click=ver_historial)
                    ]),
                    ft.Divider()
                ])
            )
        page.update()

    licitacion_input = ft.TextField(label="Número de Licitación")
    detalle_input = ft.Dropdown(
        label="Detalle de Carpeta",
        options=[
            ft.dropdown.Option("Mejora"),
            ft.dropdown.Option("Mantenimiento"),
            ft.dropdown.Option("Otros")
        ]
    )

    def agregar_carpeta_evento(e):
        if licitacion_input.value and detalle_input.value:
            agregar_carpeta(usuario, licitacion_input.value, detalle_input.value)
            licitacion_input.value = ""
            detalle_input.value = ""
            actualizar_lista()

    page.add(
        ft.Text(f"Bienvenido {usuario} — Aquí están tus carpetas"),
        licitacion_input,
        detalle_input,
        ft.ElevatedButton("Agregar Carpeta", on_click=agregar_carpeta_evento),
        ft.Divider(),
        lista_carpetas,
        ft.Divider(),
        ft.ElevatedButton("Cerrar sesión", on_click=lambda e: funcion_mostrar_inicio())
    )

    actualizar_lista()
