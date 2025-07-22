import sqlite3

# ✅ Inicializa la tabla de usuarios si no existe
def init_usuarios_db():
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            contrasena TEXT,
            rol TEXT
        )
    """)
    conn.commit()
    conn.close()

# ✅ Crea un usuario administrador por defecto si la tabla está vacía
def crear_admin_por_defecto():
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    cantidad = cursor.fetchone()[0]
    if cantidad == 0:
        cursor.execute("""
            INSERT INTO usuarios (usuario, contrasena, rol)
            VALUES (?, ?, ?)
        """, ("admin", "admin123", "ADMIN"))
        conn.commit()
    conn.close()

# ✅ Agrega un nuevo usuario (lo usa el administrador desde el panel)
def agregar_usuario(usuario, contrasena, rol):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (usuario, contrasena, rol)
        VALUES (?, ?, ?)
    """, (usuario, contrasena, rol))
    conn.commit()
    conn.close()

# ✅ Retorna todos los usuarios registrados (para mostrar en el panel de administración)
def obtener_usuarios():
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, usuario, rol FROM usuarios
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# ✅ Elimina un usuario por su ID (lo usa el panel de administrador)
def eliminar_usuario(id_usuario):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM usuarios WHERE id = ?
    """, (id_usuario,))
    conn.commit()
    conn.close()

# ✅ Valida un usuario y contraseña en el login — retorna el rol si existe, None si no
def validar_usuario_login(usuario, contrasena):
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rol FROM usuarios
        WHERE usuario = ? AND contrasena = ?
    """, (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
