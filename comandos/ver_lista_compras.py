from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import obtener_lista_compras  # ajustá el import a tu estructura

async def ver_lista_compras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    
    lista = obtener_lista_compras(telegram_id)
    
    if lista:
        mensaje = "🛒 Estos productos están en tu lista de compras:\n\n"
        mensaje += "\n".join(f"- {item.capitalize()}" for item in lista)
    else:
        mensaje = "🎉 ¡Tu heladera está completa! No hay productos con cantidad 0."

    await update.message.reply_text(mensaje)
