# Generated by Django 3.1.2 on 2022-08-27 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0060_building'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='size',
        ),
    ]
