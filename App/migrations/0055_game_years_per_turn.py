# Generated by Django 3.1.2 on 2022-03-25 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0054_notification_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='years_per_turn',
            field=models.IntegerField(default=1),
        ),
    ]
