from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import eliminar_producto, existe_usuario, producto_existe

async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("⚠️ Uso: /eliminar nombre_producto")
        return

    nombre = args[0].lower()
    telegram_id = str(update.effective_user.id)

    if not existe_usuario(telegram_id):
        await update.message.reply_text(
            "❌ No se encontró tu heladera. Por favor inicia con /start."
        )
        return

    if not producto_existe(telegram_id, nombre):
        await update.message.reply_text(
            f"⚠️ El producto '{nombre}' no está en tu heladera."
        )
        return

    eliminar_producto(telegram_id, nombre)
    await update.message.reply_text(
        f"🗑️ Producto '{nombre}' eliminado de tu heladera."
    )
