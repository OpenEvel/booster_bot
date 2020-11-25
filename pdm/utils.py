# -*- coding: utf-8 -*-
import sys
import time
import subprocess

from pathlib import Path

# Директория в которой расположены менеджеры проекта
MANAGERS_DIR = Path(__file__).resolve().parent
# Директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent


def is_win():
    """Возвращает True, если платформа - Windows"""
    return 'win' in sys.platform

def status_bar(title:str=None, *, command:str, ts:float=0.25):
    """
        title   : сообщение пользователю (что будет выводиться вместо самой комманды)
        command : комманда оболочки (что выполняется)
        ts      : интервал времени между анимацией статус бара
    """
    ENCODING_CONSOLE = 'cp1251' if is_win() else 'utf8'

    if not title:
        title = command

    write, flush = sys.stdout.write, sys.stdout.flush
    animations = ['|', '/', '-', '\\' ]  # Элементы анимации статус бара

    # Запускаем комманду command через subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    i_a = -1
    while True:
        if process.poll() is not None:
            # При работе программы были ошибки
            if process.poll() != 0:                
                if process.stderr:
                    write(f'\r\t{title}: [NO]\n')
                    write(f'command: {command}\n')
                    write('-----------------------ERROR MESSAGE---------------------\n')
                    flush()
                    while True:
                        err = process.stderr.readline()
                        err = err.decode(ENCODING_CONSOLE)

                        if err == '':
                            write('---------------------------------------------------------\n')
                            flush()
                            # Выходим из цикла вывода ошибок
                            break
                        if err != '':
                            write(f'{err}')
                            flush()
            else:
                # Прграмма завершилась нормально
                write(f'\r\t{title}: [OK]\n')
                flush()

            # Выхлодим из бесконечного цикла анимации
            break

        # Получаем индекс анимации (не выходящий за пределы массива анимаций)
        # По сути проходим по списку анимаций круг за кругом
        i_a = (i_a + 1) % len(animations)

        # Обновляем анимацию в статус баре (благодаря символу возврата каретки '\r')
        write(f'\r\t{title}: [{animations[i_a]}]')
        flush()

        # Делаем перерыв между анимациями, чтобы не получилась каша
        time.sleep(ts)
