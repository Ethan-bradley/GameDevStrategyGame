# Generated by Django 3.1.2 on 2022-02-18 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0042_auto_20220120_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='AdditionalWelfare',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='Welfare',
            field=models.FloatField(default=0.1),
        ),
    ]