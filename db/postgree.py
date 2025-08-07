import sqlitecloud
import os
from dotenv import load_dotenv
from datetime import date, timedelta 

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
        vencimiento DATE,
        FOREIGN KEY (telegram_id) REFERENCES usuarios(telegram_id)
    );
    """
    )

    conn.commit()
    print("✅ Tablas creadas correctamente.")


# ---------- CRUD USUARIOS ----------
def crear_usuario(telegram_id, nombre):
    telegram_id = str(telegram_id).strip()  # Consistencia
    nombre = nombre.strip() if nombre else ""
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
def agregar_producto(telegram_id, nombre, cantidad, vencimiento=None):
    telegram_id = str(telegram_id).strip()  # Consistencia
    nombre = nombre.strip()  # Limpiar espacios
    if vencimiento:
        cursor.execute(
            "INSERT INTO productos (telegram_id, nombre, cantidad, vencimiento) VALUES (?, ?, ?, ?)",
            (telegram_id, nombre, cantidad, vencimiento)
        )
    else:
        cursor.execute(
            "INSERT INTO productos (telegram_id, nombre, cantidad) VALUES (?, ?, ?)",
            (telegram_id, nombre, cantidad)
        )
    conn.commit()


def obtener_productos(telegram_id):
    telegram_id = str(telegram_id).strip()
    
    # Verificación de conexión para SQLite Cloud (necesario para conexiones remotas)
    try:
        cursor.execute("SELECT 1")  # Ping simple a la conexión
        cursor.fetchone()
    except Exception as e:
        print(f"[WARNING] Problema de conexión detectado: {e}")
        return []
    
    # Consulta principal
    try:
        cursor.execute(
            "SELECT id, nombre, cantidad FROM productos WHERE telegram_id = ?",
            (telegram_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] Error en consulta obtener_productos: {e}")
        return []


def buscar_producto(telegram_id, nombre_producto):
    telegram_id = str(telegram_id).strip()
    nombre_producto = nombre_producto.strip().lower()
    cursor.execute(
        """
        SELECT nombre
        FROM productos
        WHERE telegram_id = ? AND TRIM(LOWER(nombre)) = ?
        """,
        (telegram_id, nombre_producto),
    )
    resultado = cursor.fetchone()
    return resultado


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


def eliminar_producto(telegram_id, nombre):
    telegram_id = str(telegram_id).strip()
    nombre = nombre.strip().lower()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE telegram_id = ? AND LOWER(nombre) = ?
        """,
        (telegram_id, nombre)
    )
    conn.commit()
    

def obtener_productos_por_vencer(telegram_id):
    hoy = date.today()
    limite = hoy + timedelta(days=5)
    cursor.execute("""
        SELECT nombre, cantidad, vencimiento
        FROM productos
        WHERE telegram_id = ? AND vencimiento IS NOT NULL AND vencimiento BETWEEN ? AND ?
        ORDER BY vencimiento ASC
    """, (telegram_id, hoy, limite))
    return cursor.fetchall()


def vaciar_heladera(telegram_id):
    telegram_id = str(telegram_id).strip()

    cursor.execute(
        "DELETE FROM productos WHERE telegram_id = ?;",
        (telegram_id,)
    )
    conn.commit()


def actualizar_producto_nombre(telegram_id, nombre_actual, nuevo_nombre):
    telegram_id = str(telegram_id).strip()
    nombre_actual = nombre_actual.strip().lower()
    nuevo_nombre = nuevo_nombre.strip()
    cursor.execute(
        """
        UPDATE productos
        SET nombre = ?
        WHERE telegram_id = ? AND LOWER(nombre) = LOWER(?);
        """,
        (nuevo_nombre, telegram_id, nombre_actual),
    )
    conn.commit()

def actualizar_producto_cantidad(telegram_id, nombre_actual, nueva_cantidad):
    cursor.execute(
        """
        UPDATE productos
        SET cantidad = ?
        WHERE telegram_id = ? AND nombre = ?;
        """,
        (nueva_cantidad, telegram_id, nombre_actual),
    )
    conn.commit()


def obtener_productos_bajo_stock(telegram_id, umbral=2):
    telegram_id = str(telegram_id).strip()
    try:
        cursor.execute(
            """
            SELECT nombre, cantidad FROM productos
            WHERE telegram_id = ? AND cantidad <= ?
            """,
            (telegram_id, umbral)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] obtener_productos_bajo_stock: {e}")
        return []

def obtener_lista_compras(telegram_id):
    cursor.execute("""
        SELECT nombre FROM productos
        WHERE cantidad = 0 AND usuario_id = (
            SELECT id FROM usuarios WHERE telegram_id = ?
        )
    """, (telegram_id,))
    return [fila[0] for fila in cursor.fetchall()]


def producto_existe(telegram_id, nombre):
    telegram_id = str(telegram_id).strip()
    nombre = nombre.strip().lower()
    
    cursor.execute(
        """
        SELECT 1 FROM productos
        WHERE telegram_id = ? AND LOWER(nombre) = ?
        """,
        (telegram_id, nombre)
    )
    
    return cursor.fetchone() is not None

# ---------- FUNCIONES AUXILIARES ----------


# ---------- CIERRE ----------
def cerrar_conexion():
    conn.close()


# ---------- MAIN DE PRUEBA ----------
if __name__ == "__main__":
    crear_tablas()
