# Generated by Django 3.1 on 2020-08-21 13:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_lista_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lista',
            name='user',
            field=models.ManyToManyField(related_name='lista_de_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
