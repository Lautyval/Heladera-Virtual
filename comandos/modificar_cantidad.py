from telegram import Update
from telegram.ext import ContextTypes
from logica.heladera import modificar_cantidad_producto

async def modificar_cantidad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ Uso: /modificar_cantidad nombre_producto nueva_cantidad")
        return

    nombre_actual = args[0].lower()
    try:
        nueva_cantidad = int(args[1])
    except ValueError:
        await update.message.reply_text("❌ La cantidad debe ser un número.")
        return

    telegram_id = str(update.effective_user.id)
    mensaje = modificar_cantidad_producto(telegram_id, nombre_actual, nueva_cantidad)
    await update.message.reply_text(mensaje)