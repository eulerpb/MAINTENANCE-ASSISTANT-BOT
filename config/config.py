from os import getenv
from dotenv import load_dotenv #procura o arquivo .env na máquina para verificar as credenciais do telegram

import firebase_admin
from firebase_admin import credentials, firestore, storage

load_dotenv()

# autenticação do firebase
cred = credentials.Certificate('D:\Euler\Documents\PROGRAMAÇÃO\BOT TELEGRAM\hsnauticabot-firebase.json')
firebase_app = firebase_admin.initialize_app(cred, {'storageBucket': 'hsnauticabot.appspot.com'})
db = firestore.client()
storage_client = storage.bucket()

# Autenticação do Telegram
TELEGRAM_API_ID = getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = getenv("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")