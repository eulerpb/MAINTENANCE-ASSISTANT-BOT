from handlers import message_texts

async def consultarServico (Client, message, db):
    chat = message.chat

    await message.reply("Estes são os cadastros já criados:")
    docs = db.collection("Revisoes").stream()

    for doc in docs:
        await message.reply(f"{doc.id}")


    response = await chat.ask("Me informe o nome do veículo que seja consultar:")
    nomeVeiculo = response.text    

    doc_ref = db.collection("Revisoes").document(nomeVeiculo.upper())
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
    else:
        print("No such document!")

    await message.reply("Consulta finalizada! \nVocê deseja fazer mais alguma coisa? ", reply_markup = message_texts.botoes)
    


    #await app.send_photo(message.chat.id, "https://storage.googleapis.com/hsnauticabot.appspot.com/Mon%20Feb%2012%2017%3A53%3A17%202024.jpg")