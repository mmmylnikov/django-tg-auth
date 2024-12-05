# Generated by Django 5.0.3 on 2024-12-04 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tg_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='tg_photo_url',
            field=models.URLField(blank=True, null=True, verbose_name='Telegram photo URL'),
        ),
    ]