# Generated by Django 3.1.2 on 2022-09-13 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0062_auto_20220827_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='Consumption',
        ),
        migrations.RemoveField(
            model_name='game',
            name='Employment',
        ),
        migrations.RemoveField(
            model_name='game',
            name='GoodsBalance',
        ),
        migrations.RemoveField(
            model_name='game',
            name='GoodsPerCapita',
        ),
        migrations.RemoveField(
            model_name='game',
            name='Inflation',
        ),
        migrations.RemoveField(
            model_name='game',
            name='InterestRate',
        ),
        migrations.RemoveField(
            model_name='game',
            name='Resentment',
        ),
        migrations.RemoveField(
            model_name='game',
            name='ScienceArr',
        ),
    ]
