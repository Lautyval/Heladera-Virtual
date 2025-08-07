from telegram import Update
from telegram.ext import ContextTypes
from db.postgree import crear_usuario, existe_usuario


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    username = update.effective_user.first_name or "Usuario"

    comandos = (
        "Estos son los comandos que podés usar:\n"
        "/agregar - Agregar un producto a tu heladera\n"
        "/ver_heladera - Ver los productos de tu heladera\n"
        "/modificar_nombre - Modificar el nombre de un producto\n"
        "/modificar_cantidad - Modificar la cantidad de un producto\n"
        "/eliminar - Eliminar un producto de tu heladera\n"
        "/bajo_stock - Muestra productos con 2 a 0 unidades\n"
        "/vaciar_heladera - Vacia toda tu heladera\n"
        "/productos_por_vencer - Muestra productos que vencen dentro de 5 dias o menos\n"
        "/ver_lista_compras - Muestra productos con 0 unidades\n"
    )

    if existe_usuario(telegram_id):
        mensaje = (
            f"Hola {username}, con id {telegram_id} ya tienes una heladera creada.\n\n"
            f"{comandos}"
        )
    else:
        crear_usuario(telegram_id, username)
        mensaje = f"Hola {username}, creaste una nueva heladera.\n\n" f"{comandos}"

    await update.message.reply_text(mensaje)
