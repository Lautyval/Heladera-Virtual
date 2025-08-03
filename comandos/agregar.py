from telegram import Update
from telegram.ext import ContextTypes
from logica.heladera import agregar_producto

async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ Uso: /agregar nombre cantidad")
        return

    nombre = args[0]
    try:
        cantidad = int(args[1])
    except ValueError:
        await update.message.reply_text("❌ La cantidad debe ser un número.")
        return

    mensaje = agregar_producto(nombre.capitalize(), cantidad)
    await update.message.reply_text(mensaje)
