import os
import asyncio
from django.core.management.base import BaseCommand
from aiogram import Bot, executor, Dispatcher, types
from asgiref.sync import sync_to_async

from bot_tlg import logic
from bot_tlg.models import TlgBot

async def period_check_state(dp):
    """Пероидически проверяет состояние бота"""
    while True:
        bot = dp.bot
        table_bot = await logic.get_bot(bot.id)
        if table_bot.state == 'off':
            os._exit(0)
        await asyncio.sleep(2)

async def on_startup(dp):
    """При запуске бота"""

    # Выводим сообщение
    bot = dp.bot
    me = await bot.get_me()
    print(f'{me.username} запущен')

    # Записываем в базу, что бот включён
    table_bot = await logic.get_bot(bot.id)
    table_bot.state = "on"
    await sync_to_async(table_bot.save)()

    asyncio.create_task(period_check_state(dp))

def register_handlers(dp):
    """Регестрируем все нужные обработчики сообщений"""
    dp.register_message_handler(logic.on, commands=['on'])
    dp.register_message_handler(logic.off, commands=['off'])
    dp.register_message_handler(logic.status, commands=['status'])
    dp.register_message_handler(logic.run, commands=['run'])

def start_bot(token):
    bot = Bot(token)
    dp = Dispatcher(bot)

    # регестрируем нужные обработчики
    register_handlers(dp)

    @dp.message_handler()
    async def cmd(message: types.Message):
        await message.answer(message.text)

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


class Command(BaseCommand):
    help = 'Запустить телеграм-бот'

    def add_arguments(self, parser):
        parser.add_argument(
            nargs='+',
            type=int,
            dest = 'args'
        )

    def handle(self, *args, **options):
        if len(args) > 0:
            bot_pk = args[0]
            bot = TlgBot.objects.get(pk=bot_pk)
            start_bot(bot.token)

