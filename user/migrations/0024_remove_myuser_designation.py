# Generated by Django 3.0.7 on 2020-06-20 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_myuser_designation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='designation',
        ),
    ]
