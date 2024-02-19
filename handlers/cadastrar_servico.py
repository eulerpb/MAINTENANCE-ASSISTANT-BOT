import re
from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from pyromod import Client, Message 

from utils import *


#Botões de modo geral, necessário agrupar futuramente
botoes = InlineKeyboardMarkup( [
            [InlineKeyboardButton('Cadastrar novo serviço realizado', callback_data='cadastrar')],
            [InlineKeyboardButton('Consultar histórico de serviços', callback_data='consultar')],
            [InlineKeyboardButton('Sair', callback_data='sair')]
        ])

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