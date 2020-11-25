# -*- coding: utf-8 -*-
import os
import sys
from . import utils


def run_manager(python_exe, manager, *args):
    """
    Запускает определённый менеджер с аргументами
    manager: имя python файла - менеджер
    """
    # Записываем полный путь до исполняемого файла - менеджера
    manager = utils.MANAGERS_DIR / manager
    # Получаем cистемный интерпретатор python, который будет запускать менеджеры
    str_args = ' '.join(args)
    # Собираем комманду, которую нужно выполнить
    command = f'{python_exe} {manager}'
    # Если есть аргументы, то добавляем их к комманде
    if str_args:
        command += ' ' + str_args
    # запускаем комманду
    os.system(command)

def main():
    # Получаем аргументы из коммандной строки
    argv = sys.argv[1:]    
    if len(argv) == 0:
        print("Пропущены аргументы")    
    # Получаем в каком режиме была запущена утилита
    mode = argv[0]

    # Системный интерпретатор python
    python_global_exe = "python" if utils.is_win() else 'python3'
    # Устанавливаем нужные пакеты - зависимости, создаём виртуальное окружение
    # run_manager(python_global_exe, 'package_manager.py')
    
    # Интерпретатор python из виртуального окружения, созданного на предыдущем шаге
    python_exe = "venv\\Scripts\\python" if utils.is_win() else "venv/bin/python"
    python_exe = utils.BASE_DIR / python_exe
    # Устанавливаем переменные окружения для режима работы mode
    run_manager(python_exe, 'env_manager.py', mode)

__all__ = ['utils', 'main']