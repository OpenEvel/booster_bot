from django.conf import settings
from ..models import Profile
from ..models import Message
from aiogram import Dispatcher, Bot, types
import telebot

# bot = telebot.TeleBot(settings.TOKEN)

class BotsDispathcer(Bot):
    all = []

    def __init__(self, *args, **kargs):
        # Добавляем этот диспетчер в список всех диспетчеров
        BotsDispathcer.all.append(self)
        super().__init__(self, *args, **kargs)
    
    @classmethod
    def message_handler_lol(cls, *custom_filters, commands=None, regexp=None, content_types=None, state=None,
                        run_task=None, **kwargs):
        def decorator(callback):
            for dp in BotsDispathcer.all:
                dp.register_message_handler(callback, *custom_filters,
                                          commands=commands, regexp=regexp, content_types=content_types,
                                          state=state, run_task=run_task, **kwargs)
            return callback

        return decorator


@BotsDispathcer.message_handler_lol()
async def cmd(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    print(text)

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
