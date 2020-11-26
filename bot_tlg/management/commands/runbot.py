from django.core.management.base import BaseCommand
from bot_tlg import logic
from bot_tlg.models import TlgBot
from aiogram import Bot, executor, Dispatcher, types

async def on_startup(dp):
    bot = dp.bot
    try:
        me = await bot.get_me()
        print(f'{me.username} запущен')
    except:
        pass

def star_bot(token):
    bot = Bot(token)
    dp = Dispatcher(bot)

    dp.register_message_handler(logic.on, commands=['on'])
    dp.register_message_handler(logic.off, commands=['off'])
    dp.register_message_handler(logic.status, commands=['status'])
    dp.register_message_handler(logic.run, commands=['run'])

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
            star_bot(bot.token)
