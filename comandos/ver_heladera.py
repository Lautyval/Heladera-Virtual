from db.postgree import obtener_productos
from telegram import Update
from telegram.ext import ContextTypes


async def ver_heladera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    telegram_id = str(update.effective_user.id)
    
    # Llamar a la función original
    productos = obtener_productos(telegram_id)    
    # Probar la lógica de ver_heladera_texto
    if not productos:
        mensaje = "🧊 Tu heladera está vacía."
    else:
        mensaje = "🥶 Tu heladera contiene:\n"
        for prod in productos:
            mensaje += f"- {prod[1].capitalize()} x{prod[2]}\n"
        mensaje = mensaje.strip()
    await update.message.reply_text(mensaje)