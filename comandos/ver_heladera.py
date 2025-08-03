from telegram import Update
from telegram.ext import ContextTypes
from logica.heladera import ver_heladera

async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = ver_heladera()
    await update.message.reply_text(mensaje)
