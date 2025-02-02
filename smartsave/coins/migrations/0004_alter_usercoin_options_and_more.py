# Generated by Django 5.1.3 on 2024-11-09 12:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0003_remove_coin_api_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercoin',
            options={'verbose_name': 'Пользовательские накопления'},
        ),
        migrations.AlterUniqueTogether(
            name='usercoin',
            unique_together={('user', 'coin')},
        ),
    ]
