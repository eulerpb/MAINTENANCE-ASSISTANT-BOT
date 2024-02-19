import re
from pyrogram.types import (ReplyKeyboardMarkup)

from firebase_admin import firestore, storage
import time

from models import message_texts


async def cadastroServico (Client, message, db):
    chat = message.chat

    response = await chat.ask("Certo. Vamos iniciar o cadastro. Por favor me informe o Nome do veículo:")
    nomeVeiculo = response.text

    response = await chat.ask("A qual cliente pertence o veículo?")
    nomeCliente = response.text

    response = await chat.ask("Ok. agora me informe quantas horas rodadas do veículo:")
    kmVeiculo = response.text

    dataManutencao = None
    while dataManutencao == None:
        response = await chat.ask("Agora, por favor, me diga a data da última revisão feita:")
        formatoData = re.compile(r'\d{2}/\d{2}/\d{4}')
        if re.match(formatoData, response.text):
            dataManutencao = response.text
        else:
            await message.reply("Por favor, digite novamente a data no formato dd/mm/aaaa")
            dataManutencao = None

    response = await chat.ask("Ótimo, agora me informe qual o tipo de serviço que foi feito:", reply_markup=message_texts.tipos_servicos)
    tipoServico = response.text

    response = await chat.ask("Qual o valor que foi cobrado pelo serviço?")
    valorRevisao = response.text

    response = await chat.ask("Você deseja anexar fotos do serviço?", reply_markup=message_texts.cliente_concorda)
    if response.text == "Sim":
        response = await chat.ask("Por favor, envie a foto do serviço.")
        if response.photo:
            photo_bytes = await response.download()
            imagem = await upload_photo(photo_bytes)
            await message.reply("A foto foi armazenada com sucesso no Firebase Storage!")
        else:
            await message.reply("Você não enviou uma imagem. Gostaria de tentar novamente?")
            imagem = 0
            

    await message.reply("""
                        Obrigado pelas respostas! Gostaria apenas que me confirmasse as informações:
                        \n**Nome do veículo:** {}
                        \n**Nome do cliente:** {}
                        \n**KM do veiculo:** {} Km
                        \n**Data da manutencao:** {}
                        \n**Serviço realizado:** {}
                        \n**Valor da manutenção:** R$ {}""".format(nomeVeiculo, nomeCliente, kmVeiculo, dataManutencao, tipoServico, valorRevisao))

    # Mensagem final
    await message.reply("Cadastro concluído com sucesso! \nVocê deseja fazer mais alguma coisa? ", reply_markup = message_texts.botoes)
    cadastrarDados(db, nomeVeiculo, nomeCliente, kmVeiculo, dataManutencao, tipoServico, valorRevisao, imagem, message.chat.username)

def cadastrarDados(db, nomeVeiculo, nomeCliente, kmVeiculo, dataManutencao, tipoServico, valorRevisao, urlImagem, username):
    doc_ref = db.collection("Revisoes").document(nomeVeiculo.upper())
    doc_ref.set({
        "nome veículo": nomeVeiculo.upper(),
        "registros": firestore.ArrayUnion([{
            "nome cliente": nomeCliente.upper(),
            "KM veiculo": kmVeiculo,
            "data manutencao": dataManutencao,
            "tipo do servico": tipoServico.upper(),
            "valor da manutenção": valorRevisao,
            "Imagem anexada:": urlImagem,
            "cadastrado por": username
        }])
    }, merge=True)

async def upload_photo(photo_bytes):
    filename = f"{time.asctime()}.jpg"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(photo_bytes)

    blob.make_public()
    url = blob.public_url
    return url