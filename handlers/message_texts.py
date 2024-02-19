from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


texto_boasVindas = """
Olá, bom dia! em que posso lhe ajudar hoje? \n
Ou selecione uma das opções abaixo:"""


botoes = InlineKeyboardMarkup( [
            [InlineKeyboardButton('Cadastrar novo serviço realizado', callback_data='cadastrar')],
            [InlineKeyboardButton('Consultar histórico de serviços', callback_data='consultar')],
            [InlineKeyboardButton('Sair', callback_data='sair')]
        ])