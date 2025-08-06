from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import obtener_productos_bajo_stock, existe_usuario

async def bajo_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    if not existe_usuario(telegram_id):
        await update.message.reply_text("❌ No se encontró tu heladera. Usá /start primero.")
        return

    productos = obtener_productos_bajo_stock(telegram_id, umbral=2)

    if not productos:
        await update.message.reply_text("🎉 No hay productos con bajo stock.")
    else:
        mensaje = "📉 Productos con bajo stock:\n"
        for nombre, cantidad in productos:
            mensaje += f"- {nombre.capitalize()} ({cantidad})\n"
        await update.message.reply_text(mensaje.strip())
