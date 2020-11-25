# -*- coding: utf-8 -*-
import os
import sys
import string
import secrets
import dotenv

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdm import utils

# Путь до настроок переменных окружения
ENV_PATH = utils.BASE_DIR / ".env"

def new_secret_key(count=50):
    """Создаёт новую строку секретного ключа"""
    # Создадим свой набор символов, из которого получим SECRET_KEY
    chars = string.digits + string.ascii_lowercase + string.punctuation
    # Удалим из этого набора ненужные символы
    black_list = ("\'", '"', '`', '\\')
    for c in black_list:
        chars = chars.replace(c, '')    
    # Получим секретный ключ при помощи специальной библиотеки secrets
    secret_key = ''.join(secrets.choice(chars) for _ in range(count))
    return secret_key

def main():
    # Получаем аргументы из коммандной строки
    argv = sys.argv[1:]
    
    if len(argv) == 0:
        print("Пропущены аргументы при использвании env_manager")
    # Получаем в каком режиме была запущена утилита
    mode = argv[0]
    
    # Если не существует .env файла, то создаём его
    if not os.path.exists(ENV_PATH):
        ENV_PATH.touch()

    # Загружаем переменные окружения
    dotenv.load_dotenv()

    # Задаём переменную SECRET_KEY, чтобы django мог создать базу
    # Чтобы не перезаписывать переменную проверяем задана ли она
    if not os.getenv('SECRET_KEY', default=False):
        dotenv.set_key(ENV_PATH, 'SECRET_KEY', new_secret_key())
    
    # Перезагружаем переменные окружения
    dotenv.load_dotenv()

    if mode == "prod":
        # На продакшене нам не нужен дебаг
        if os.getenv('DEBUG', default=False):
            dotenv.unset_key(ENV_PATH, "DEBUG")
    elif mode == 'dev':
        # При разработке включаем дебаг
        dotenv.set_key(ENV_PATH, 'DEBUG', 'on')


if __name__ == "__main__":
    main()