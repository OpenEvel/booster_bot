import os
from aiogram import types
from asgiref.sync import sync_to_async

from ..models import Profile
from ..models import Message
from ..models import TlgBot

async def get_bot(bot_id):
    get_table_bot = lambda : TlgBot.objects.get(external_id=bot_id)
    table_bot = await sync_to_async(get_table_bot)()
    return table_bot

async def on(message: types.Message):
    bot_id = message.bot.id
    table_bot = await get_bot(bot_id)
    table_bot.state = "on"
    await sync_to_async(table_bot.save)()

async def off(message: types.Message):
    bot_id = message.bot.id
    table_bot = await get_bot(bot_id)
    table_bot.state = "off"
    await sync_to_async(table_bot.save)()

async def status(message: types.Message):
    bot_id = message.bot.id
    table_bot = await get_bot(bot_id)
    if table_bot.state == 'off':
        await message.answer('Бот в состоянии "off"')
    else:
        await message.answer('Бот в состоянии "on"')

async def run(message: types.Message):
    bot_id = message.bot.id
    table_bot = await get_bot(bot_id)
    if table_bot.state == 'off':
        await message.answer('Иди нахуй я ливаю')
        os._exit(0)
    else:
        await message.answer('Ещё побуду здесь')


# def cmd(message):
#     chat_id = message.chat.id
#     text = message.text

#     p, _ = Profile.objects.get_or_create(
#         external_id=chat_id,
#         defaults={
#             'name': message.from_user.username
#         }
#     )
#     # Сохраняем сообщение в базу
#     Message(profile=p, text=text).save()

#     messages =  Message.objects.filter(profile=p)
#     count = messages.count()

#     all_mess = '\n'.join([m.text for m in messages])

#     bot.send_message(chat_id, f'У вас {count} сообщений в базе\n{all_mess}')
