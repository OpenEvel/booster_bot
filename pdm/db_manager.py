# -*- coding: utf-8 -*-
"""Менеджер для настройки базы данных"""
import os
import sys
import django

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pdm import utils

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booster_suite.settings")
django.setup()
from django.conf import settings
# Получаем путь до базы данных
DB_PATH = settings.DATABASES['default']['NAME']

def main():
    # Если база данных существует
    if os.path.exists(DB_PATH):
        # то удаляем её
        os.remove(DB_PATH)

    # Создаём нужные миграции
    utils.status_bar('make migrations for DB', 
                     command = f'{utils.VENV_PY_EXE} {utils.BASE_DIR / "manage.py"} migrate')
    
    # Создаём супер пользователя
    os.system(f'{utils.VENV_PY_EXE} {utils.BASE_DIR / "manage.py"} createsuperuser')

if __name__ == "__main__":
    main()