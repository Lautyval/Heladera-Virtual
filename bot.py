import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from comandos.agregar import agregar

from comandos.ver_heladera import ver

from comandos.modificar import modificar


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bienvenido a tu heladera virtual.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agregar", agregar))
    app.add_handler(CommandHandler("ver_heladera", ver))
    app.add_handler(CommandHandler("modificar", modificar))



    print("✅ Bot funcionando...")
    app.run_polling()
