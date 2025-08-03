import sqlitecloud
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api = os.getenv("API_SQLITE")

# Conexión global
conn = sqlitecloud.connect(api)
cursor = conn.cursor()

# ---------- CREACIÓN DE TABLAS ----------
def crear_tablas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS heladeras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        heladera_id INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (heladera_id) REFERENCES heladeras(id)
    );
    """)

    conn.commit()
    print("✅ Tablas creadas correctamente.")

# ---------- CRUD USUARIOS ----------
def crear_usuario(telegram_id):
    cursor.execute("INSERT OR IGNORE INTO usuarios (telegram_id) VALUES (?);", (telegram_id,))
    conn.commit()

    cursor.execute("SELECT id FROM usuarios WHERE telegram_id = ?;", (telegram_id,))
    user_id = cursor.fetchone()[0]

    cursor.execute("INSERT OR IGNORE INTO heladeras (usuario_id) VALUES (?);", (user_id,))
    conn.commit()

def obtener_usuario_por_id(usuario_id):
    cursor.execute("SELECT * FROM usuarios WHERE id = ?;", (usuario_id,))
    return cursor.fetchone()

def obtener_todos_los_usuarios():
    cursor.execute("SELECT * FROM usuarios;")
    return cursor.fetchall()


def actualizar_usuario(usuario_id, nuevo_telegram_id):
    try:
        cursor.execute("UPDATE usuarios SET telegram_id = ? WHERE id = ?;", (nuevo_telegram_id, usuario_id))
        conn.commit()
        print("✅ Usuario actualizado.")
    except Exception as e:
        print("❌ Error al actualizar:", e)

def eliminar_usuario(usuario_id):
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = ?;", (usuario_id,))
        conn.commit()
        print("🗑️ Usuario eliminado.")
    except Exception as e:
        print("❌ Error al eliminar:", e)

# ---------- CRUD PRODUCTOS ----------
def agregar_producto(heladera_id, nombre, cantidad):
    cursor.execute("""
    INSERT INTO productos (heladera_id, nombre, cantidad)
    VALUES (?, ?, ?);
    """, (heladera_id, nombre, cantidad))
    conn.commit()

def obtener_productos(heladera_id):
    cursor.execute("""
    SELECT id, nombre, cantidad
    FROM productos
    WHERE heladera_id = ?;
    """, (heladera_id,))
    return cursor.fetchall()

def actualizar_producto(producto_id, nueva_cantidad):
    cursor.execute("""
    UPDATE productos
    SET cantidad = ?
    WHERE id = ?;
    """, (nueva_cantidad, producto_id))
    conn.commit()

def eliminar_producto(producto_id):
    cursor.execute("DELETE FROM productos WHERE id = ?;", (producto_id,))
    conn.commit()

# ---------- FUNCIONES AUXILIARES ----------
def obtener_heladera_id(telegram_id):
    cursor.execute("""
    SELECT h.id
    FROM heladeras h
    JOIN usuarios u ON h.usuario_id = u.id
    WHERE u.telegram_id = ?;
    """, (telegram_id,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

# ---------- CIERRE ----------
def cerrar_conexion():
    conn.close()

# ---------- MAIN DE PRUEBA ----------
if __name__ == "__main__":
    crear_tablas()