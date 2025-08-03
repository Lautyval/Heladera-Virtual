import json
import os

RUTA_ARCHIVO = os.path.join("db", "heladera.json")

def cargar_heladera():
    if not os.path.exists(RUTA_ARCHIVO):
        return []
    with open(RUTA_ARCHIVO, "r") as f:
        return json.load(f)

def guardar_heladera(productos):
    with open(RUTA_ARCHIVO, "w") as f:
        json.dump(productos, f, indent=4)

def agregar_producto(nombre, cantidad):
    productos = cargar_heladera()

    # Buscar si ya existe
    for prod in productos:
        if prod["nombre"] == nombre:
            prod["cantidad"] += cantidad
            guardar_heladera(productos)
            return f"🔄 Se actualizó {nombre} a {prod['cantidad']} unidades."

    # Si no existe, agregar nuevo
    productos.append({"nombre": nombre, "cantidad": cantidad})
    guardar_heladera(productos)
    return f"✅ Producto agregado: {nombre} x{cantidad}"

def ver_heladera():
    productos = cargar_heladera()
    if not productos:
        return "🧊 Tu heladera está vacía."

    mensaje = "🥶 Tu heladera contiene:\n"
    for prod in productos:
        mensaje += f"- {prod['nombre']} x{prod['cantidad']}\n"
    return mensaje.strip()

def modificar_producto(nombre_actual, nuevo_nombre=None, nueva_cantidad=None):
    productos = cargar_heladera()
    actualizado = False

    for producto in productos:
        if producto["nombre"].lower() == nombre_actual.lower():
            if nuevo_nombre:
                producto["nombre"] = nuevo_nombre.lower()
            if nueva_cantidad is not None:
                producto["cantidad"] = nueva_cantidad
            actualizado = True
            break

    if actualizado:
        guardar_heladera(productos)
        return "✅ Producto modificado correctamente."
    else:
        return "❌ Producto no encontrado en tu heladera."
