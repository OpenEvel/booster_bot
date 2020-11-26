from django.core.management.base import BaseCommand
from bot_tlg.logic import BotsDispathcer
from bot_tlg.models import TlgBot
from aiogram import Bot, executor, Dispatcher
import asyncio

def main():
    all_bots = TlgBot.objects.all()
    for bot in all_bots:
        b = Bot(bot.token)
        # dp = BotsDispathcer(b)
        # executor.start_polling(dp, skip_updates=True)

async def lol(TOKEN):
    bot = Bot(TOKEN)
    try:
        me = await bot.get_me()
        print(f'{me.username} запущен')
    finally:
        await bot.close()


class Command(BaseCommand):
    help = 'Запустить телеграм-бот'

    def handle(self, *args, **options):
        TOKEN = TlgBot.objects.all()[0].token
        asyncio.run(lol(TOKEN))