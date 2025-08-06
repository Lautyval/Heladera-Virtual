from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import agregar_producto, existe_usuario
from datetime import datetime

async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ Uso: /agregar <nombre> <cantidad> [vencimiento YYYY-MM-DD]")
        return

    nombre = args[0].lower()
    try:
        cantidad = int(args[1])
    except ValueError:
        await update.message.reply_text("❌ La cantidad debe ser un número.")
        return

    vencimiento = None
    if len(args) >= 3:
        try:
            # Validamos que la fecha sea correcta
            vencimiento = datetime.strptime(args[2], "%Y-%m-%d").date()
        except ValueError:
            await update.message.reply_text("⚠️ Fecha inválida. Usa el formato YYYY-MM-DD.")
            return

    telegram_id = str(update.effective_user.id)

    if not existe_usuario(telegram_id):
        await update.message.reply_text(
            "❌ No se encontró tu heladera. Por favor inicia con /start."
        )
        return

    agregar_producto(telegram_id, nombre, cantidad, vencimiento)

    mensaje = f"✅ Se agregó {cantidad} de {nombre.capitalize()} a tu heladera."
    if vencimiento:
        mensaje += f" (vencimiento: {vencimiento})"
    await update.message.reply_text(mensaje)

