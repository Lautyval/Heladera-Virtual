import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db.postgree import crear_tablas
from comandos.start import start

from comandos.agregar import agregar
from comandos.ver_heladera import ver_heladera
from comandos.modificar_nombre import modificar_nombre
from comandos.modificar_cantidad import modificar_cantidad
from comandos.eliminar import eliminar
from comandos.productos_por_vencer import productos_por_vencer
from comandos.vaciar_heladera import vaciar
from comandos.bajo_stock import bajo_stock
from comandos.ver_lista_compras import ver_lista_compras


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


if __name__ == "__main__":
    crear_tablas()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agregar", agregar))
    app.add_handler(CommandHandler("ver_heladera", ver_heladera))
    app.add_handler(CommandHandler("modificar_nombre", modificar_nombre))
    app.add_handler(CommandHandler("modificar_cantidad", modificar_cantidad))
    app.add_handler(CommandHandler("eliminar", eliminar))
    app.add_handler(CommandHandler("productos_por_vencer", productos_por_vencer))
    app.add_handler(CommandHandler("vaciar_heladera", vaciar))
    app.add_handler(CommandHandler("bajo_stock", bajo_stock))
    app.add_handler(CommandHandler("ver_lista_compras", ver_lista_compras))


    print("✅ Bot funcionando...")
    app.run_polling()
