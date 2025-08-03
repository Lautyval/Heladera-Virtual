import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from comandos.start import start

from comandos.agregar import agregar

from comandos.ver_heladera import ver

from comandos.modificar import modificar


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agregar", agregar))
    app.add_handler(CommandHandler("ver_heladera", ver))
    app.add_handler(CommandHandler("modificar", modificar))



    print("✅ Bot funcionando...")
    app.run_polling()
