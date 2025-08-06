from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import vaciar_heladera, existe_usuario

async def vaciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    if not existe_usuario(telegram_id):
        await update.message.reply_text(
            "❌ No se encontró tu heladera. Por favor inicia con /start."
        )
        return

    vaciar_heladera(telegram_id)
    await update.message.reply_text("🧹 Tu heladera fue vaciada con éxito.")
