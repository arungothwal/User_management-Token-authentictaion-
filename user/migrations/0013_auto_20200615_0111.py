# Generated by Django 3.0.7 on 2020-06-15 08:11

from django.db import migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20200615_0108'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
    ]
