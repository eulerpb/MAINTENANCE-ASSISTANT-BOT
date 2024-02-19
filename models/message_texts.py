from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup)


texto_boasVindas = """
Olá, bom dia! em que posso lhe ajudar hoje? \n
Ou selecione uma das opções abaixo:"""


botoes = InlineKeyboardMarkup( [
            [InlineKeyboardButton('Cadastrar novo serviço realizado', callback_data='cadastrar')],
            [InlineKeyboardButton('Consultar histórico de serviços', callback_data='consultar')],
            [InlineKeyboardButton('Sair', callback_data='sair')]
        ])

tipos_servicos = ReplyKeyboardMarkup(
        [
            ['Troca de óleo', 'Revisão simples'],
            ['Manutenção preventiva', 'Substituição de peças'],
            ['Instalação de motor', 'Retirada de motor', 'Troca de motor'],
            ['Instalação de gerador', 'Retirada de gerador', 'Revisão de gerador'],
            ['']
        ], resize_keyboard=False
    )

cliente_concorda = ReplyKeyboardMarkup(
        [
            ['Sim', 'Não'],
            ['']
        ], resize_keyboard=False
    )