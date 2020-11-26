from django.db import models
from django.db.models.fields import TextField
from django.utils import version

class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в телеграме",
        unique=True,
    )
    name = models.TextField(verbose_name="Имя пользователя")

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"

class Message(models.Model):
    profile = models.ForeignKey(
        to='bot_tlg.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural= 'Сообщения'
    
class TlgBot(models.Model):

    username = models.TextField(
        verbose_name='Логин'
    )

    external_id = models.PositiveIntegerField(
        verbose_name="ID бота в телеграме",
        unique=True,
    )
    
    token = models.TextField(
        verbose_name='Токен'
    )

    state = models.TextField(
        verbose_name='Состояние',
        default = 'off',
    )

    class Meta:
        verbose_name="Телеграм бот"
        verbose_name_plural="Телеграм боты"