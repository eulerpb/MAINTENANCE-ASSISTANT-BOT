from os import getenv
from dotenv import load_dotenv #procura o arquivo .env na máquina para verificar as credenciais do telegram

import time

from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from pyromod import Client, Message


import firebase_admin
from firebase_admin import credentials, firestore, storage

import re #regex para aplicar o formato da data

load_dotenv()

# autenticação do firebase
cred = credentials.Certificate('D:\Euler\Documents\PROGRAMAÇÃO\BOT TELEGRAM\hsnauticabot-firebase.json')
firebase_app = firebase_admin.initialize_app(cred, {'storageBucket': 'hsnauticabot.appspot.com'})
db = firestore.client()

storage_client = storage.bucket()


#autenticação
app = Client("HS nautica", 
             api_id = getenv("TELEGRAM_API_ID"), 
             api_hash = getenv("TELEGRAM_API_HASH"),
             bot_token = getenv("TELEGRAM_BOT_TOKEN"))

texto_boasVindas = """
Olá, bom dia! em que posso lhe ajudar hoje? \n
Digite /Cadastrar - Para cadastrar um novo serviço realizado \n 
Digite /Consultar - para consultar o histórico de seviços \n
Digite /Sair - a qualquer momento para encerrar a conversa \n
Ou selecione uma das opções abaixo:"""

boasVindas2 = "Olá, bom dia! em que posso lhe ajudar hoje? Agora utilizando botões"
textoConsultar = "Certo. Para consultar o histórico preciso que me informe qual a referência do veículo:"

botoes = InlineKeyboardMarkup( [
            [InlineKeyboardButton('Cadastrar novo serviço realizado', callback_data='cadastrar')],
            [InlineKeyboardButton('Consultar histórico de serviços', callback_data='consultar')],
            [InlineKeyboardButton('Sair', callback_data='sair')]
        ])

id_inicio_mensagem = None
id_fim_mensagem = None

#Resposta ao ser enviado qualquer mensagem pelo usuário
@app.on_message()
async def messages(Client, message):

    global id_inicio_mensagem, id_fim_mensagem
    if id_inicio_mensagem is None:
        id_inicio_mensagem = message.id
    
    await message.reply(texto_boasVindas, reply_markup = botoes)


@app.on_message(filters.command('Cadastrar'))
async def cadastroServico (Client, message):
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

    response = await chat.ask("Ótimo, agora me informe qual o tipo de serviço que foi feito:", reply_markup=ReplyKeyboardMarkup(
        [
            ['Troca de óleo', 'Revisão simples'],
            ['Manutenção preventiva', 'Substituição de peças'],
            ['Instalação de motor', 'Retirada de motor', 'Troca de motor'],
            ['Instalação de gerador', 'Retirada de gerador', 'Revisão de gerador'],
            ['']
        ], resize_keyboard=False
    ))
    tipoServico = response.text

    response = await chat.ask("Qual o valor que foi cobrado pelo serviço?")
    valorRevisao = response.text

    response = await chat.ask("Você deseja anexar fotos do serviço?", reply_markup=ReplyKeyboardMarkup(
        [
            ['Sim', 'Não'],
            ['']
        ], resize_keyboard=False
    ))
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
    await message.reply("Cadastro concluído com sucesso! \nVocê deseja fazer mais alguma coisa? ", reply_markup = botoes)
    cadastrarDados(nomeVeiculo, nomeCliente, kmVeiculo, dataManutencao, tipoServico, valorRevisao, imagem, message.chat.username)

#Função para cadastrar as informações no firebase
def cadastrarDados(nomeVeiculo, nomeCliente, kmVeiculo, dataManutencao, tipoServico, valorRevisao, urlImagem, username):
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

@app.on_message(filters.command('Consultar'))
async def consultarServico (Client, message):
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

    await message.reply("Consulta finalizada! \nVocê deseja fazer mais alguma coisa? ", reply_markup = botoes)
    


    #await app.send_photo(message.chat.id, "https://storage.googleapis.com/hsnauticabot.appspot.com/Mon%20Feb%2012%2017%3A53%3A17%202024.jpg")


@app.on_message(filters.command('Sair'))
async def end_chat(Client, message):
    global id_inicio_mensagem, id_fim_mensagem
    chat_id = message.chat.id
    id_fim_mensagem = message.id

    await message.reply("Estou encerrando o chat! Qualquer coisa estarei à disposição! \nCaso precise de suporte novamente pode mandar um Oi!")
    if id_inicio_mensagem and id_fim_mensagem:
        await Client.delete_messages(chat_id, range(id_inicio_mensagem-1, id_fim_mensagem + 1))
        id_inicio_mensagem = None
        id_fim_mensagem = None
    await app.leave_chat(chat_id, delete=True)

@app.on_callback_query()
async def escolher_Opcoes(Client, callback_query):
    opcaoEscolhida = callback_query.data
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id

    match opcaoEscolhida:
        case "cadastrar":
            await app.delete_messages(chat_id, message_id)
            await cadastroServico(Client, callback_query.message)
        case "consultar":
            await consultarServico(Client, callback_query.message)
        case "sair":
            await app.delete_messages(chat_id, message_id)
            await end_chat(Client, callback_query.message)


async def upload_photo(photo_bytes):
    filename = f"{time.asctime()}.jpg"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(photo_bytes)

    blob.make_public()
    url = blob.public_url
    return url


app.run()