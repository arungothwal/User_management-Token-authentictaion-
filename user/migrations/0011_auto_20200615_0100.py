# Generated by Django 3.0.7 on 2020-06-15 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200615_0010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
