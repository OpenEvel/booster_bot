def pre_start():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booster_suite.settings')
    import django
    django.setup()

pre_start()
from bot_tlg.logic import bot

if __name__ == "__main__":
    bot.infinity_polling()
