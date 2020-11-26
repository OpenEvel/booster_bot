# -*- coding: utf-8 -*-
"""Менеджер для установки пакетов-зависимостей"""
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdm import utils

def main():
    # Создаём виртуальное окружение
    utils.status_bar("making 'venv' directory", 
                     command=f"{utils.G_PY_EXE} -m venv {utils.VENV_PATH}")
     # Устанавливаем нужные для работы бота библиотеки
    print("\tpip installing requirements(python libraries):")
    for lib in open(utils.BASE_DIR / 'requirements.txt', 'r', encoding='utf8'):
        # Очищаем строку с названием библиотеки от пробельных символов
        lib = lib.strip()
        # Статус бар для каждой отдельной библиотеки
        utils.status_bar(f"\t* {lib}", command=f"{utils.VENV_PIP} install {lib}")


if __name__ == "__main__":
    main()