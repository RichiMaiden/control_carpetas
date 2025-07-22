import sqlite3
from datetime import datetime
import csv

def init_db():
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carpetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            licitacion TEXT,
            detalle TEXT,
            estado TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_carpeta INTEGER,
            accion TEXT,
            detalle TEXT,
            fecha TEXT,
            FOREIGN KEY (id_carpeta) REFERENCES carpetas(id)
        )
    """)
    conn.commit()
    conn.close()

def agregar_carpeta(usuario, licitacion, detalle, estado="Enviada"):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO carpetas (usuario, licitacion, detalle, estado)
        VALUES (?, ?, ?, ?)
    """, (usuario, licitacion, detalle, estado))
    conn.commit()
    conn.close()

def obtener_carpetas_por_usuario(usuario):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, licitacion, detalle, estado FROM carpetas
        WHERE usuario = ?
    """, (usuario,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def actualizar_estado_carpeta(id_carpeta, nuevo_estado):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE carpetas SET estado = ? WHERE id = ?
    """, (nuevo_estado, id_carpeta))
    conn.commit()
    conn.close()
    registrar_historial(id_carpeta, "Cambio de Estado", f"Nuevo estado: {nuevo_estado}")

def eliminar_carpeta(id_carpeta):
    registrar_historial(id_carpeta, "Eliminación", "Carpeta eliminada")
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM carpetas WHERE id = ?
    """, (id_carpeta,))
    conn.commit()
    conn.close()

def registrar_historial(id_carpeta, accion, detalle):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historial (id_carpeta, accion, detalle, fecha)
        VALUES (?, ?, ?, ?)
    """, (id_carpeta, accion, detalle, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def obtener_historial_por_carpeta(id_carpeta):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT accion, detalle, fecha FROM historial
        WHERE id_carpeta = ?
        ORDER BY fecha DESC
    """, (id_carpeta,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_todas_las_carpetas():
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, usuario, licitacion, detalle, estado FROM carpetas
    """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def exportar_carpetas_a_csv(nombre_archivo="carpetas_exportadas.csv"):
    datos = obtener_todas_las_carpetas()
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["ID", "Usuario", "Licitación", "Detalle", "Estado"])
        for fila in datos:
            writer.writerow(fila)
