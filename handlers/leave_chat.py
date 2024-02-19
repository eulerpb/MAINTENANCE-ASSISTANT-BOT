async def end_chat(Client, message, app, id_inicio_mensagem, id_fim_mensagem):
    chat_id = message.chat.id
    id_fim_mensagem = message.id

    await message.reply("Estou encerrando o chat! Qualquer coisa estarei à disposição! \nCaso precise de suporte novamente pode mandar um Oi!")
    if id_inicio_mensagem and id_fim_mensagem:
        await Client.delete_messages(chat_id, range(id_inicio_mensagem-1, id_fim_mensagem + 1))
        id_inicio_mensagem = None
        id_fim_mensagem = None
    await app.leave_chat(chat_id, delete=True)