# Generated by Django 3.1.2 on 2022-09-13 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0063_auto_20220913_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='Capital',
        ),
        migrations.RemoveField(
            model_name='player',
            name='Employment',
        ),
        migrations.RemoveField(
            model_name='player',
            name='GDP',
        ),
        migrations.RemoveField(
            model_name='player',
            name='GDPGrowth',
        ),
        migrations.RemoveField(
            model_name='player',
            name='GDPPerCapita',
        ),
        migrations.RemoveField(
            model_name='player',
            name='GoodsPerCapita',
        ),
        migrations.RemoveField(
            model_name='player',
            name='GoodsProduction',
        ),
        migrations.RemoveField(
            model_name='player',
            name='GovBudget',
        ),
        migrations.RemoveField(
            model_name='player',
            name='Inflation',
        ),
        migrations.RemoveField(
            model_name='player',
            name='InterestRate',
        ),
        migrations.RemoveField(
            model_name='player',
            name='RealGDP',
        ),
        migrations.RemoveField(
            model_name='player',
            name='tradeBalance',
        ),
    ]
