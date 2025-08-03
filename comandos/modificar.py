from telegram import Update
from telegram.ext import ContextTypes
from logica.heladera import modificar_producto

async def modificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text[len("/modificar "):].strip()

    if " por " not in texto:
        await update.message.reply_text("⚠️ Formato incorrecto. Usá: /modificar producto_viejo por producto_nuevo [cantidad]")
        return

    partes = texto.split(" por ")

    if len(partes) != 2:
        await update.message.reply_text("⚠️ No pude entender el mensaje. Usá: /modificar producto_viejo por producto_nuevo [cantidad]")
        return

    nombre_actual = partes[0].strip()
    resto = partes[1].strip().split()

    nuevo_nombre = " ".join(resto[:-1]) if resto[-1].isdigit() else " ".join(resto)
    nueva_cantidad = int(resto[-1]) if resto[-1].isdigit() else None

    mensaje = modificar_producto(nombre_actual, nuevo_nombre, nueva_cantidad)
    await update.message.reply_text(mensaje)

