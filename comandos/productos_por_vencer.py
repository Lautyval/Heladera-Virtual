from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import obtener_productos_por_vencer, existe_usuario

async def productos_por_vencer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    if not existe_usuario(telegram_id):
        await update.message.reply_text(
            "❌ No se encontró tu heladera. Por favor inicia con /start."
        )
        return

    productos = obtener_productos_por_vencer(telegram_id)

    if not productos:
        await update.message.reply_text("🎉 No tenés productos por vencer en los próximos 5 días.")
        return

    mensaje = "⏳ Productos por vencer en los próximos 5 días:\n"
    for nombre, cantidad, vencimiento in productos:
        mensaje += f"• {nombre.capitalize()} ({cantidad}) - vence el {vencimiento}\n"

    await update.message.reply_text(mensaje)
