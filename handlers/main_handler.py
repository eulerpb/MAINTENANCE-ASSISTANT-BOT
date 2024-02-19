from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from pyromod import Client, Message

from models import message_texts
from handlers import consultar_servico
from handlers import cadastrar_servico
from handlers import leave_chat

def executar_app(app, db):
    global id_inicio_mensagem, id_fim_mensagem
    id_inicio_mensagem = None
    id_fim_mensagem = None

    @app.on_message()
    async def messages(Client, message):

        global id_inicio_mensagem, id_fim_mensagem
        if id_inicio_mensagem is None:
            id_inicio_mensagem = message.id
        
        await message.reply(message_texts.texto_boasVindas, reply_markup = message_texts.botoes)


    @app.on_callback_query()
    async def escolher_Opcoes(Client, callback_query):
        opcaoEscolhida = callback_query.data
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.id

        match opcaoEscolhida:
            case "cadastrar":
                await app.delete_messages(chat_id, message_id)
                await cadastrar_servico.cadastroServico(Client, callback_query.message, db)
            case "consultar":
                await app.delete_messages(chat_id, message_id)
                await consultar_servico.consultarServico(Client, callback_query.message, db)
            case "sair":
                await app.delete_messages(chat_id, message_id)
                await leave_chat.end_chat(Client, callback_query.message, app, id_inicio_mensagem, id_fim_mensagem)