# Generated by Django 3.1.3 on 2020-11-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_tlg', '0003_auto_20201113_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='ID пользователя в телеграме'),
        ),
    ]
