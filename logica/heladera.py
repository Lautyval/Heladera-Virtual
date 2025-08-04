from db.postgree import (
    buscar_producto,
    actualizar_producto_nombre,
    actualizar_producto_cantidad,
    obtener_productos,
)

def ver_heladera(telegram_id):
    productos = obtener_productos(telegram_id)
    if not productos:
        return "🧊 Tu heladera está vacía."

    mensaje = "🥶 Tu heladera contiene:\n"
    for prod in productos:
        mensaje += (
            f"- {prod[1].capitalize()} x{prod[2]}\n"  # prod[1]=nombre, prod[2]=cantidad
        )
    return mensaje.strip()


def modificar_nombre_producto(telegram_id, nombre_actual, nuevo_nombre):
    nombre_actual = nombre_actual.strip().lower()
    nuevo_nombre = nuevo_nombre.strip().lower()

    producto = buscar_producto(telegram_id, nombre_actual)
    if not producto:
        return "❌ No se encontró el producto en tu heladera."

    actualizar_producto_nombre(telegram_id, nombre_actual, nuevo_nombre)
    return f"✅ Producto renombrado a: {nuevo_nombre.capitalize()}"


def modificar_cantidad_producto(telegram_id, nombre_actual, nueva_cantidad):
    producto = buscar_producto(telegram_id, nombre_actual.lower())
    if not producto:
        return "❌ No se encontró el producto en tu heladera."
    actualizar_producto_cantidad(telegram_id, nombre_actual.lower(), nueva_cantidad)
    return f"✅ Cantidad actualizada a: {nueva_cantidad}"
