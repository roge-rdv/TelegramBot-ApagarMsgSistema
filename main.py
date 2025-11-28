from telethon import TelegramClient
from telethon.tl.types import MessageActionChatJoinedByLink, MessageActionChatDeleteUser
import asyncio
import os
from dotenv import load_dotenv

# 🔑 API do Telegram
load_dotenv()  # carrega variáveis de um .env se presente

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_name = os.getenv("TG_SESSION")
target_group = int(os.getenv("TARGET_GROUP"))
bot_token = os.getenv("TG_BOT_TOKEN")  # opcional: use para iniciar como bot

client = TelegramClient(session_name, api_id, api_hash)

# Se um token de bot for fornecido, inicia o cliente com ele antes do contexto `with client:`
if bot_token:
    client.start(bot_token=bot_token)


async def main():
    async for message in client.iter_messages(target_group):
        if isinstance(message.action, (MessageActionChatJoinedByLink, MessageActionChatDeleteUser)) or \
           'entrou no grupo via link de convite' in (message.message or '') or \
           'saiu do grupo' in (message.message or ''):
            try:
                await client.delete_messages(target_group, message.id)
                print(f'Deletado: {message.id}')
            except Exception as e:
                print(f'Erro ao deletar {message.id}: {e}')

with client:
    client.loop.run_until_complete(main())
