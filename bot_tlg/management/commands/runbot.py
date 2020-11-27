import os
import sys
import asyncio
import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand
from aiogram import Bot, executor, Dispatcher, types
from asgiref.sync import sync_to_async

from bot_tlg import logic
from bot_tlg.models import TlgBot

BASE_DIR = Path(__file__).parent.parent.parent.parent
# Интерпретатор python из виртуального окружения
VENV_PY_EXE = "venv\\Scripts\\python" if 'win' in sys.platform else "venv/bin/python"
VENV_PY_EXE = BASE_DIR / VENV_PY_EXE

async def period_check_state(dp):
    """Пероидически проверяет состояние бота"""
    while True:
        bot = dp.bot
        try:
            table_bot = await logic.get_bot(bot.id)
        except TlgBot.DoesNotExist:
            # Мы попоали в исключение, значит такого бота нет в таблице
            # Поэтому просто завершаем процесс
            os._exit(0)

        # Бот есть в базе, смотрим его состояние
        if table_bot.state == 'off':
            os._exit(0)
        await asyncio.sleep(2)

async def on_startup(dp):
    """При запуске бота"""

    # Выводим сообщение
    bot = dp.bot
    me = await bot.get_me()
    print(f'{me.username} {me.id} запущен')

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

def start_bot(bot_pk):
    table_bot = TlgBot.objects.get(pk=bot_pk)
    bot = Bot(table_bot.token)
    dp = Dispatcher(bot)

    # регестрируем нужные обработчики
    register_handlers(dp)

    @dp.message_handler()
    async def cmd(message: types.Message):
        await message.answer(message.text)

    executor.start_polling(dp, on_startup=on_startup)

def bot_at_proc(*args):
    """Запуск бота в отдельном процессе"""
    runner = BASE_DIR / 'manage.py'
    command = f'{VENV_PY_EXE} {runner} runbot'
    # Собираем все позиционные аргументы в строку
    str_args = ' '.join(str(x) for x in args)
    if str_args:
        command += ' ' + str_args
    # Запускам бота в отдельном процессе
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc


class Command(BaseCommand):
    help = 'Запустить телеграм-бот'

    def add_arguments(self, parser):
        # Добавляем опцию - запустить в отдельном процессе
        parser.add_argument(
            '-p', 
            '--process',
            action='store_true', 
            default=False,
            help='Запуск в отдельном процессе'
        )

        # Добавляем позиционный параметр - запустить бота по его 
        # primary key в базе данных
        parser.add_argument(
            nargs='*',
            type=int,
            dest='args'
        )

    def handle(self, *args, **options):
        if options['process']:
            # Запускаем ОДНОГО бота в отдельном процессе
            bot_at_proc(*args)
        elif len(args) == 1:
            # Запускаем бота в ЭТОМ процессе
            bot_pk = args[0]
            start_bot(bot_pk)
        elif len(args) > 1:
            # Запускаем всех ботов из списка args
            for bot_pk in args:
                bot_at_proc(bot_pk)
        else:
            # Не было передано никаких параметров
            # Запускаем всех ВЫКЛЮЧЕННЫХ ботов из базы данных
            print('Запускаю всех выключенных ботов')
            for bot in TlgBot.objects.filter(state='off'):
                bot_at_proc(bot.pk)


