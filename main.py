from pyrogram import Client
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN
from handlers import cadastroServico, consultarServico

# Inicializa o cliente Pyrogram
app = Client("HS nautica", 
             api_id=TELEGRAM_API_ID, 
             api_hash=TELEGRAM_API_HASH,
             bot_token=TELEGRAM_BOT_TOKEN)

cadastroServico()
consultarServico()

# Inicia a execução do bot
app.run()