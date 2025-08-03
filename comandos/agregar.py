from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import agregar_producto, existe_usuario


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

    telegram_id = str(update.effective_user.id)

    if not existe_usuario(telegram_id):
        await update.message.reply_text(
            "❌ No se encontró tu heladera. Por favor inicia con /start."
        )
        return

    agregar_producto(telegram_id, nombre.capitalize(), cantidad)
    await update.message.reply_text(
        f"✅ Se agregó {cantidad} de {nombre.capitalize()} a tu heladera."
    )
