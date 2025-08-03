import sqlitecloud
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api = os.getenv("API_SQLITE")

# Conexión global
conn = sqlitecloud.connect(api)
cursor = conn.cursor()


def crear_tablas():
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS usuarios (
        telegram_id TEXT PRIMARY KEY,
        nombre TEXT
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (telegram_id) REFERENCES usuarios(telegram_id)
    );
    """
    )

    conn.commit()
    print("✅ Tablas creadas correctamente.")


# ---------- CRUD USUARIOS ----------
def crear_usuario(telegram_id, nombre):
    print(f"Creando usuario: {telegram_id} - {nombre}")
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (telegram_id, nombre) VALUES (?, ?);",
        (telegram_id, nombre),
    )
    conn.commit()


def buscar_usuario(telegram_id):
    print(f"Buscando usuario: {telegram_id}")
    cursor.execute(
        "SELECT telegram_id FROM usuarios WHERE telegram_id = ?;", (telegram_id,)
    )
    return cursor.fetchone() is not None


def obtener_usuario_por_id(telegram_id):
    cursor.execute("SELECT * FROM usuarios WHERE telegram_id = ?;", (telegram_id,))
    return cursor.fetchone()


def obtener_todos_los_usuarios():
    cursor.execute("SELECT * FROM usuarios;")
    return cursor.fetchall()


def existe_usuario(telegram_id):
    cursor.execute(
        "SELECT telegram_id FROM usuarios WHERE telegram_id = ?;", (telegram_id,)
    )
    return cursor.fetchone() is not None


def actualizar_usuario(telegram_id, nuevo_nombre):
    try:
        cursor.execute(
            "UPDATE usuarios SET nombre = ? WHERE telegram_id = ?;",
            (nuevo_nombre, telegram_id),
        )
        conn.commit()
        print("✅ Usuario actualizado.")
    except Exception as e:
        print("❌ Error al actualizar:", e)


def eliminar_usuario(telegram_id):
    try:
        cursor.execute("DELETE FROM usuarios WHERE telegram_id = ?;", (telegram_id,))
        conn.commit()
        print("🗑️ Usuario eliminado.")
    except Exception as e:
        print("❌ Error al eliminar:", e)


# ---------- CRUD PRODUCTOS ----------
def agregar_producto(telegram_id, nombre, cantidad):
    cursor.execute(
        """
    INSERT INTO productos (telegram_id, nombre, cantidad)
    VALUES (?, ?, ?);
    """,
        (telegram_id, nombre, cantidad),
    )
    conn.commit()


def obtener_productos(telegram_id):
    cursor.execute(
        """
    SELECT id, nombre, cantidad
    FROM productos
    WHERE telegram_id = ?;
    """,
        (telegram_id,),
    )
    return cursor.fetchall()


def actualizar_producto(producto_id, nueva_cantidad):
    cursor.execute(
        """
    UPDATE productos
    SET cantidad = ?
    WHERE id = ?;
    """,
        (nueva_cantidad, producto_id),
    )
    conn.commit()


def eliminar_producto(producto_id):
    cursor.execute("DELETE FROM productos WHERE id = ?;", (producto_id,))
    conn.commit()


# ---------- FUNCIONES AUXILIARES ----------
# Ya no necesitas obtener_heladera_id, puedes eliminarla.


# ---------- CIERRE ----------
def cerrar_conexion():
    conn.close()


# ---------- MAIN DE PRUEBA ----------
if __name__ == "__main__":
    crear_tablas()
