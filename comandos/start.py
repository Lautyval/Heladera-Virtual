from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import crear_usuario, existe_usuario


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    username = update.effective_user.first_name or "Usuario"

    if existe_usuario(telegram_id):
        mensaje = (
            f"Hola {username}, con id {telegram_id} ya tienes una heladera creada.\n\n"
            "Estos son los comandos que podés usar:\n"
            "/agregar - Agregar un producto a tu heladera\n"
            "/ver_heladera - Ver los productos de tu heladera\n"
            "/modificar - Modificar productos existentes\n"
        )
    else:
        crear_usuario(telegram_id, username)
        mensaje = (
            f"Hola {username}, creaste una nueva heladera.\n\n"
            "Estos son los comandos que podés usar:\n"
            "/agregar - Agregar un producto a tu heladera\n"
            "/ver_heladera - Ver los productos de tu heladera\n"
            "/modificar - Modificar productos existentes\n"
        )

    await update.message.reply_text(mensaje)
