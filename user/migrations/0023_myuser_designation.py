# Generated by Django 3.0.7 on 2020-06-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_auto_20200618_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='designation',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]