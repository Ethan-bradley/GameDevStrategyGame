# Generated by Django 3.1.2 on 2022-03-25 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0055_game_years_per_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='projection_unloaded',
            field=models.BooleanField(default=True),
        ),
    ]