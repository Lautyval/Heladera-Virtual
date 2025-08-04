from telegram import Update
from telegram.ext import ContextTypes
from logica.heladera import modificar_nombre_producto

async def modificar_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ Uso: /modificar_nombre nombre_actual nuevo_nombre")
        return

    nombre_actual = args[0].strip().lower()
    nuevo_nombre = " ".join(args[1:]).strip().lower()
    telegram_id = str(update.effective_user.id)
    print(f"Telegram ID: {telegram_id}, Nombre actual: {nombre_actual}, Nuevo nombre: {nuevo_nombre}")
    mensaje = modificar_nombre_producto(telegram_id, nombre_actual, nuevo_nombre)
    await update.message.reply_text(mensaje)