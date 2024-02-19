from os import getenv
from dotenv import load_dotenv #procura o arquivo .env na máquina para verificar as credenciais do telegram

import firebase_admin
from firebase_admin import credentials, firestore, storage

from pyrogram import Client

from handlers import main_handler

load_dotenv()

# autenticação do firebase
cred = credentials.Certificate('D:\Euler\Documents\PROGRAMAÇÃO\BOT TELEGRAM\config\hsnauticabot-firebase.json')
firebase_app = firebase_admin.initialize_app(cred, {'storageBucket': 'hsnauticabot.appspot.com'})
db = firestore.client()
storage_client = storage.bucket()

# Inicializa o cliente Pyrogram
app = Client("HS nautica", 
             api_id = getenv("TELEGRAM_API_ID"), 
             api_hash = getenv("TELEGRAM_API_HASH"),
             bot_token = getenv("TELEGRAM_BOT_TOKEN"))

main_handler.executar_app(app, db)

# Inicia a execução do bot
app.run()