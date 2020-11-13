from django.conf import settings
from .models import Profile
from .models import Message
import telebot

bot = telebot.TeleBot(settings.TOKEN)

@bot.message_handler()
def cmd(message):
    chat_id = message.chat.id
    text = message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': message.from_user.username
        }
    )
    # Сохраняем сообщение в базу
    Message(profile=p, text=text).save()

    messages =  Message.objects.filter(profile=p)
    count = messages.count()

    all_mess = '\n'.join([m.text for m in messages])

    bot.send_message(chat_id, f'У вас {count} сообщений в базе\n{all_mess}')
