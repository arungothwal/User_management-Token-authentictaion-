# Generated by Django 3.0.7 on 2020-06-13 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200613_0813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='myuser',
            old_name='staff',
            new_name='is_staff',
        ),
    ]
